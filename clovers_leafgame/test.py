from PIL import Image
from io import BytesIO

# 假设binary_data是你的二进制图像数据
binary_data = b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x04\x00\x00\x00\x04\x08\x02\x00\x00\x00$BZ\xf6\x00\x00\x00\x01sRGB\x00\xae\xce\x1c\xe9\x00\x00\x00\x04gAMA\x00\x00\xb1\x8f\x0b\xfca\x05\x00\x00\x00\tpHYs\x00\x00\x0e\xc3\x00\x00\x0e\xc3\x01\xc7o\xa8d\x00\x00\x00\x19tEXtSoftware\x00www.inkspace.com\x00\x00\x00\x00IDATx\x9c\xed\xd1\t\x800\x0c\x85\xff\xbd\xfe\x17f\x08 \x10\x04\x81\x00\x01\x03\x02\x00\x07oF\xd8\x0f\xf2\x1b\x00\x00\x00\x00IEND\xaeB`\x82"

# 使用BytesIO创建一个类似文件的对象
image_stream = BytesIO(binary_data)

# 使用Image.open打开二进制图像数据
image = Image.open(image_stream)

# 进行后续操作，比如显示图像
image.show()
