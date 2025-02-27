import cv2
import os
import concurrent.futures
# nohup python test_multi.py > output.log 2>&1 &
# 定义文件路径
input_dir = '/data/xdan/datasets/xdan-video-collections/istock_v3'
output_dir = '/data/xdan/datasets/xdan-video-collections-v3-2fp-multi-nh'

# 创建输出目录（如果不存在的话）
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

# 获取目录中的所有视频文件
video_files = [f for f in os.listdir(input_dir) if f.endswith('.mp4') or f.endswith('.avi')]  # 根据实际视频文件类型调整

if not video_files:
    print("没有找到视频文件！")
else:
    # 定义视频处理函数
    def process_video(video_file):
        input_video_path = os.path.join(input_dir, video_file)

        # 读取视频
        cap = cv2.VideoCapture(input_video_path)
        if not cap.isOpened():
            print(f"无法打开视频文件: {input_video_path}")
            return
        
        # 获取视频的原始帧率
        original_fps = cap.get(cv2.CAP_PROP_FPS)
        print(f"处理视频: {video_file}, 原始帧率: {original_fps} fps")
        
        # 设置新的帧率为 2 帧每秒
        new_fps = 2

        # 获取视频的其他信息
        frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 使用 mp4v 编码器
        
        # 设置输出视频路径
        output_video_path = os.path.join(output_dir, f"{video_file}")
        out = cv2.VideoWriter(output_video_path, fourcc, new_fps, (frame_width, frame_height))

        frame_count = 0
        while True:
            ret, frame = cap.read()
            if not ret:
                break

            # 只提取符合新帧率的帧
            if frame_count % int(original_fps / new_fps) == 0:
                out.write(frame)

            frame_count += 1

        # 释放资源
        cap.release()
        out.release()
        print(f"视频已保存到: {output_video_path}")

    # 使用 ThreadPoolExecutor 来创建 100 个线程并行处理视频
    with concurrent.futures.ThreadPoolExecutor(max_workers=100) as executor:
        # 提交所有视频任务
        futures = [executor.submit(process_video, video_file) for video_file in video_files]
        
        # 等待所有线程完成
        concurrent.futures.wait(futures)
        print("finished!")
        # 可以通过 futures.result() 获取每个线程的执行结果，如果有需要的话
        
video_files_input = [f for f in os.listdir(input_dir) if f.endswith('.mp4') or f.endswith('.avi')]  # 根据实际视频文件类型调整
video_files_output = [f for f in os.listdir(output_dir) if f.endswith('.mp4') or f.endswith('.avi')] 
# 输出视频文件的数量
print("input", len(video_files_input))
print("output", len(video_files_output))

