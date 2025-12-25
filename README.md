# 多信通自定义ComfyUI节点库 (dxt-custom-nodes)

多信通的自定义ComfyUI节点库，用于支持AI内容生成平台的业务功能需求，提供Alibaba Cloud OSS上传等核心功能。

## 功能特性

- **图片上传节点**: 将ComfyUI生成的图片上传到OSS
- **视频上传节点**: 将视频(兼容VideoHelperSuite)上传到OSS
- **音频上传节点**: 将音频文件上传到OSS
- **自动重试**: 上传失败时自动重试，最多重试20次
- **随机文件名生成**: 可选择生成带时间戳的随机文件名
- **自定义文件名**: 可选择指定自定义文件名
- **可配置的OSS设置**: 支持自定义端点、存储桶、访问密钥和路径

## 安装

1. 将 `dxt-custom-nodes` 文件夹复制到您的 ComfyUI `custom_nodes` 目录中
2. 安装所需依赖：
   ```bash
   pip install -r requirements.txt
   ```

## 使用方法

### 阿里云OSS图片上传节点 (Aliyun OSS Image Uploader)

**输入参数：**
- `image`: 来自ComfyUI的IMAGE类型
- `endpoint`: OSS端点 (例如: https://oss-cn-hangzhou.aliyuncs.com)
- `bucket`: OSS存储桶名称
- `access_key`: Access Key ID
- `access_secret`: Access Key Secret
- `path`: OSS存储路径 (例如: comfyui/images)
- `random_filename`: 是否启用随机文件名生成的布尔值
- `filename`: 自定义文件名 (当random_filename为False时使用)

**输出：**
- `urls`: 上传到OSS的文件的完整URL，多个文件用逗号分隔

### 阿里云OSS音频上传节点 (Aliyun OSS Audio Uploader)

**输入参数：**
- `audio`: 来自ComfyUI的AUDIO类型
- `endpoint`: OSS端点 (例如: https://oss-cn-hangzhou.aliyuncs.com)
- `bucket`: OSS存储桶名称
- `access_key`: Access Key ID
- `access_secret`: Access Key Secret
- `path`: OSS存储路径 (例如: comfyui/audio)
- `random_filename`: 是否启用随机文件名生成的布尔值
- `filename`: 自定义文件名 (当random_filename为False时使用)

**输出：**
- `url`: 上传到OSS的文件的完整URL

### 阿里云OSS视频上传节点 (Aliyun OSS Video Uploader)

**输入参数：**
- `video`: 来自VideoHelperSuite VideoCombine节点的VHS_FILENAMES类型
- `endpoint`: OSS端点 (例如: https://oss-cn-hangzhou.aliyuncs.com)
- `bucket`: OSS存储桶名称
- `access_key`: Access Key ID
- `access_secret`: Access Key Secret
- `path`: OSS存储路径 (例如: comfyui/videos)
- `random_filename`: 是否启用随机文件名生成的布尔值
- `filename`: 自定义文件名 (当random_filename为False时使用)

**输出：**
- `url`: 上传到OSS的文件的完整URL

## Random Filename Format

When random filename is enabled, files are named with the format:
```
{timestamp}_{random_string}.{extension}
```
Example: `20241210_143052_a3k9m2p7.png`

## Example Workflow

1. Generate an image using ComfyUI nodes
2. Connect the IMAGE output to the OSS Image Uploader node
3. Configure your OSS credentials and settings
4. Run the workflow
5. The node will output the complete OSS URL of the uploaded file

## Security Notes

- Keep your OSS access keys secure
- Consider using STS tokens for production use
- Set appropriate bucket permissions
- Use HTTPS endpoints for secure uploads

## Compatibility

- Tested with ComfyUI
- Compatible with VideoHelperSuite for video uploads
- Supports common image formats: PNG, JPG, JPEG, WebP
- Supports common video formats: MP4, AVI, MOV, WebM, MKV
- Supports common audio formats: WAV, MP3, FLAC
