"""
AI提取模块 - 使用智谱AI进行智能信息提取
"""
import json
from typing import List, Dict, Optional
from zhipuai import ZhipuAI


class AIExtractor:
    """使用智谱AI GLM-4进行信息提取"""

    def __init__(self, api_key: str):
        """
        初始化AI提取器
        :param api_key: 智谱AI的API密钥
        """
        self.client = ZhipuAI(api_key=api_key)
        self.model = "glm-4"  # 使用GLM-4模型

    def extract_information(
        self,
        document_text: str,
        fields: List[Dict[str, str]]
    ) -> Dict[str, Optional[str]]:
        """
        从文档中提取指定字段的信息
        :param document_text: 文档文本内容
        :param fields: 字段列表，格式为 [{"name": "字段名", "description": "字段描述"}, ...]
        :return: 提取结果，格式为 {"字段名": "提取的值", ...}
        """
        # 构建字段列表文本
        fields_text = ""
        result_template = {}
        for idx, field in enumerate(fields, 1):
            field_name = field.get("name", "")
            field_desc = field.get("description", "")
            fields_text += f"{idx}. {field_name}"
            if field_desc:
                fields_text += f" - {field_desc}"
            fields_text += "\n"
            result_template[field_name] = None

        # 构建提示词
        prompt = f"""你是一个专业的信息提取助手。请仔细阅读以下文档内容，并提取指定的信息字段。

文档内容：
{document_text}

需要提取的字段：
{fields_text}

要求：
1. 仔细阅读文档，提取准确的信息
2. 如果某个字段在文档中找不到，返回null
3. 提取的信息应该是原文中的内容，不要编造
4. 日期格式统一为YYYY-MM-DD
5. 如果有多个值（如参会人员），用逗号分隔

请严格按照以下JSON格式返回结果（只返回JSON，不要有其他内容）：
{json.dumps(result_template, ensure_ascii=False, indent=2)}
"""

        try:
            # 调用智谱AI API
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.1,  # 降低温度以提高准确性
            )

            # 提取响应内容
            result_text = response.choices[0].message.content.strip()

            # 尝试解析JSON
            # 有时AI会返回markdown格式的JSON，需要清理
            if result_text.startswith("```json"):
                result_text = result_text.replace("```json", "").replace("```", "").strip()
            elif result_text.startswith("```"):
                result_text = result_text.replace("```", "").strip()

            result = json.loads(result_text)
            return result

        except json.JSONDecodeError as e:
            # JSON解析失败，尝试提取关键信息
            print(f"JSON解析失败: {e}")
            print(f"AI返回内容: {result_text}")
            # 返回空结果
            return result_template

        except Exception as e:
            print(f"AI提取失败: {e}")
            raise ValueError(f"AI信息提取失败: {str(e)}")


# 测试代码
if __name__ == "__main__":
    # 测试示例
    api_key = "your-api-key-here"
    extractor = AIExtractor(api_key)

    # 示例文档
    sample_text = """
    合作协议

    甲方：北京科技有限公司
    乙方：上海创新企业

    项目名称：AI智能助手开发项目

    合作期限：
    开始日期：2024年1月1日
    结束日期：2024年12月31日

    参与人员：张三、李四、王五
    """

    # 字段定义
    fields = [
        {"name": "公司名称", "description": "合作方公司全称"},
        {"name": "项目名称", "description": "合作的项目名称"},
        {"name": "合作开始日期", "description": "合作起始日期"},
        {"name": "合作结束日期", "description": "合作终止日期"},
        {"name": "参会人员", "description": "参与人员姓名列表"}
    ]

    # 提取信息
    result = extractor.extract_information(sample_text, fields)
    print(json.dumps(result, ensure_ascii=False, indent=2))
