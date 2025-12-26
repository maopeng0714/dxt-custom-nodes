from .cloud.aliyun_oss_uploader import *
from .remote_t2i import RemoteT2iGenerator

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique

NODE_CLASS_MAPPINGS = {
    "AliyunOSSImageUploader": AliyunOSSImageUploader,
    "AliyunOSSVideoUploader": AliyunOSSVideoUploader,
    "AliyunOSSAudioUploader": AliyunOSSAudioUploader,
    "RemoteT2iGenerator": RemoteT2iGenerator
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "AliyunOSSImageUploader": "阿里云OSS图片上传",
    "AliyunOSSVideoUploader": "阿里云OSS视频上传",
    "AliyunOSSAudioUploader": "阿里云OSS音频上传",
    "RemoteT2iGenerator": "远程文生图openai兼容图像生成"
}
