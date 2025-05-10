import socket
import threading
import os
import json
import argparse
import logging
from utils import setup_logger, ensure_dir

# 服务器配置常量
DEFAULT_HOST = '0.0.0.0'                            # 监听所有网络接口
DEFAULT_PORT = 65432
DEFAULT_SAVE_DIR = 'serverinfo/server_files'        # 文件存储目录
BUFFER_SIZE = 4096                                  # 数据传输缓冲区大小
MAX_CONNECTIONS = 5                                 # 最大并发连接数

# 全局logger
logger = setup_logger()

def get_file_list(directory_path: str) -> list:
    """ 获取指定目录下的文件列表，包含文件名和大小 """
    files_info = []
    try:
        for filename in os.listdir(directory_path):
            filepath = os.path.join(directory_path, filename)
            if os.path.isfile(filepath):
                files_info.append({
                    "name": filename,
                    "size": os.path.getsize(filepath)
                })
    except OSError as e:
        logger.error(f"无法访问目录 '{directory_path}': {e}")
    return files_info


def handle_client_request(client_socket: socket.socket, client_address: tuple, save_dir: str):
    """ 处理单个客户端的连接和请求 """
    logger.info(f"接受来自 {client_address} 的连接。")

    try:
        while True:
            # 接收命令头部 (例如: "COMMAND|payload_info")
            initial_data = client_socket.recv(BUFFER_SIZE)
            if not initial_data:
                logger.info(f"客户端 {client_address} 断开连接。")
                break

            request_str = initial_data.decode('utf-8').strip()
            logger.debug(f"来自 {client_address} 的原始请求: {request_str[:100]}")

            parts = request_str.split('|', 1)
            command = parts[0]
            payload_str = parts[1] if len(parts) > 1 else ""

            # 根据命令执行不同操作
            if command == "LIST_FILES":
                logger.info(f"{client_address} 请求文件列表。")
                files = get_file_list(save_dir)
                response_data = json.dumps(files).encode('utf-8')

                # 发送响应头部：状态码|数据长度
                response_header = f"OK_LIST|{len(response_data)}".encode('utf-8')

                client_socket.sendall(response_header)
                client_socket.send(b'\n')
                client_socket.sendall(response_data)

                logger.info(f"已向 {client_address} 发送文件列表。")

            elif command == "DOWNLOAD_FILE":
                filename = payload_str
                filepath = os.path.join(save_dir, filename)
                logger.info(f"{client_address} 请求下载文件: {filename}")

                if os.path.isfile(filepath):
                    filesize = os.path.getsize(filepath)
                    # 响应：OK_DOWNLOAD|filesize
                    response_header = f"OK_DOWNLOAD|{filesize}".encode('utf-8')

                    client_socket.sendall(response_header)
                    client_socket.send(b'\n')

                    with open(filepath, 'rb') as f:
                        while True:
                            chunk = f.read(BUFFER_SIZE)
                            if not chunk:
                                break
                            client_socket.sendall(chunk)
                    logger.info(f"文件 '{filename}' ({filesize}字节) 已发送给 {client_address}。")
                
                else:
                    error_msg = f"ERROR|文件 '{filename}' 未找到。"
                    client_socket.sendall(error_msg.encode('utf-8'))
                    logger.error(f"请求的文件 '{filename}' 未找到，已告知 {client_address}。")

            elif command == "UPLOAD_FILE" or command == "UPDATE_FILE":
                try:
                    filename, filesize_str = payload_str.split('|', 1)
                    filesize = int(filesize_str)

                except ValueError:
                    error_msg = "ERROR|无效的文件上传请求格式 (应为 filename|filesize)。"
                    client_socket.sendall(error_msg.encode('utf-8'))
                    logger.error(f"{client_address} 发送了无效的上传请求: {payload_str}")
                    continue    # 这里不能用 break 要继续等待下一个命令

                filepath = os.path.join(save_dir, filename)
                file_exists = os.path.exists(filepath)
                operation_type = "更新" if (command == "UPDATE_FILE" or file_exists) else "上传"
                
                logger.info(f"{client_address} 准备{operation_type}文件: {filename} ({filesize}字节)。")

                # 告知客户端可以开始发送文件
                client_socket.sendall(b"READY_TO_RECEIVE")
                client_socket.send(b'\n')

                received_bytes = 0
                try:
                    with open(filepath, 'wb') as f:
                        while received_bytes < filesize:
                            chunk = client_socket.recv(BUFFER_SIZE)
                            if not chunk:
                                logger.error(f"{client_address} 在{operation_type}文件 '{filename}' 时连接中断。")
                                
                                # 可以考虑删除不完整的文件

                                if os.path.exists(filepath):
                                    os.remove(filepath)
                                return # 结束此客户端处理线程

                            f.write(chunk)
                            received_bytes += len(chunk)
                    
                    if received_bytes == filesize:
                        success_msg = f"OK|文件 '{filename}' 已成功{operation_type}。"
                        client_socket.sendall(success_msg.encode('utf-8'))
                        logger.info(f"文件 '{filename}' ({filesize}字节) 已从 {client_address} 接收并{operation_type}。")
                    
                    else:
                        # 文件接收不完整
                        logger.warning(f"文件 '{filename}' 从 {client_address} 接收不完整。预期 {filesize}, 收到 {received_bytes}")
                        error_msg = f"ERROR|文件 '{filename}' 接收不完整。"
                        try:
                            client_socket.sendall(error_msg.encode('utf-8'))
                        except socket.error:
                            pass # 客户端可能已关闭连接
                        if os.path.exists(filepath):
                             os.remove(filepath) # 删除不完整的文件

                except Exception as e:
                    error_msg = f"ERROR|服务器{operation_type}文件 '{filename}' 时出错: {e}"
                    logger.error(f"{operation_type}来自 {client_address} 的文件 '{filename}' 失败: {e}")
                    try:
                        client_socket.sendall(error_msg.encode('utf-8'))
                    except socket.error:
                        pass
                    if os.path.exists(filepath): # 如果出错，删除可能已创建的不完整文件
                        os.remove(filepath)
            
            else:
                error_msg = f"ERROR|未知命令: {command}"
                client_socket.sendall(error_msg.encode('utf-8'))
                logger.warning(f"{client_address} 发送了未知命令: {command}")

    except socket.error as e:
        logger.error(f"与客户端 {client_address} 通信时发生套接字错误: {e}")
    except Exception as e:
        logger.critical(f"处理客户端 {client_address} 请求时发生意外错误: {e}")
    finally:
        logger.info(f"关闭与 {client_address} 的连接。")
        client_socket.close()


def start_server(host: str, port: int, save_dir: str):
    """启动文件服务器"""
    # 1. 确保文件存储目录存在
    try:
        ensure_dir(save_dir)
    except Exception:
        logger.critical(f"无法初始化文件存储目录 '{save_dir}'。服务器将退出。")
        return

    # 2. 创建套接字并绑定
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    # 设置 SO_REUSEADDR 选项，以便在服务器快速重启时可以立即重用相同的地址和端口
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        server_socket.bind((host, port))
        server_socket.listen(MAX_CONNECTIONS)
        logger.info(f"服务器已在 {host}:{port} 启动，监听中...")
        logger.info(f"文件将保存在: {os.path.abspath(save_dir)}")
    except socket.error as e:
        logger.error(f"服务器启动失败: {e}")
        return
    except Exception as e:
        logger.error(f"服务器启动过程中发生未知错误: {e}")
        return

    # 3. 循环接受客户端连接
    try:
        while True:
            try:
                client_socket, client_address = server_socket.accept()
                # 为每个客户端连接创建一个新线程进行处理，使得服务器可以同时服务多个客户端
                client_thread = threading.Thread(
                    target=handle_client_request,
                    args=(client_socket, client_address, save_dir)
                )
                client_thread.daemon = True # 设置为守护线程，主线程退出时子线程也退出
                client_thread.start()

            except socket.error as e:
                # 在非阻塞模式下，accept 可能会抛出错误
                logger.warning(f"接受连接时出错: {e}")
                if not server_socket.fileno() == -1: # 检查套接字是否仍然有效
                    continue
                else:
                    logger.error("监听套接字已失效，服务器将停止。")
                    break

            except KeyboardInterrupt:
                logger.info("检测到 Ctrl + C，服务器准备关闭...")
                break # 用户自己中断，跳出主循环
    
    finally:
        logger.info("服务器正在关闭所有连接...")
        server_socket.close()
        logger.info("服务器已成功关闭。")
        # 确保所有日志都已写入文件
        logging.shutdown()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="简易文件服务器")
    parser.add_argument(
        "--host",
        type=str,
        default=DEFAULT_HOST,
        help=f"服务器监听的主机地址 (默认: {DEFAULT_HOST})"
    )

    parser.add_argument(
        "--port",
        type=int,
        default=DEFAULT_PORT,
        help=f"服务器监听的端口号 (默认: {DEFAULT_PORT})"
    )

    parser.add_argument(
        "--dir",
        type=str,
        default=DEFAULT_SAVE_DIR,
        help=f"文件存储和读取的目录 (默认: {DEFAULT_SAVE_DIR})"
    )

    args = parser.parse_args()

    # 启动服务器
    start_server(args.host, args.port, args.dir) 