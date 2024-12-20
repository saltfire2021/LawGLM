## 14号API接口函数 	根据案号查询文本摘要
``` 
def get_legal_abstract(query_conds: dict,need_fields: List[str] = []) -> dict:
    """
    根据案号查询文本摘要。

    参数:
    query_conds -- 查询条件字典，例如{"案号": "（2019）沪0115民初61975号"}
    need_fields -- 需要返回的字段列表，例如["文件名","案号","文本摘要"],need_fields传入空列表，则表示返回所有字段，否则返回填入的字段

    例如：
        输入：
        {"案号": "（2019）沪0115民初61975号"}
        输出：
        {'文件名': '（2019）沪0115民初61975号.txt',
        '案号': '（2019）沪0115民初61975号',
        '文本摘要': '原告上海爱斯达克汽车空调系统有限公司与被告上海逸测检测技术服务有限公司因服务合同纠纷一案，原告请求被告支付检测费1,254,802.58元、延迟履行违约金71,399.68元及诉讼费用。被告辩称，系争合同已终止，欠款金额应为499,908元，且不认可违约金。\n法院认为，原告与腾双公司签订的测试合同适用于原被告，原告提供的测试服务应得到被告支付。依照《中华人民共和国合同法》第六十条、第一百零九条,《中华人民共和国民事诉讼法》第六十四条第一款,《最高人民法院关于适用〈中华人民共和国民事诉讼法〉的解释》第九十条之规定判决被告支付原告检测费1,254,802.58元及违约金71,399.68元。'}
    """
    url = f"https://{DOMAIN}/law_api/s1_b/get_legal_abstract"
    case_num = query_conds['案号']
    if isinstance(case_num, str):
        case_num = case_num.replace('（', '(').replace('）', ')')

    if isinstance(case_num, list):
        new_case_num = []
        for ele in case_num:
            new_case_num.append(ele.replace('（', '(').replace('）', ')'))
        case_num = new_case_num
    data = {
        "query_conds": query_conds,
        "need_fields": need_fields
    }

    rsp = requests.post(url, json=data, headers=headers)
    return rsp.json()
``` 

### 例子： 
### 1
#### 输入
``` 
{"案号": "（2019）沪0115民初61975号", "need_fields":[]}
``` 
#### 输出 
``` 
{'文件名': '（2019）沪0115民初61975号.txt',
        '案号': '（2019）沪0115民初61975号',
        '文本摘要': '原告上海爱斯达克汽车空调系统有限公司与被告上海逸测检测技术服务有限公司因服务合同纠纷一案，原告请求被告支付检测费1,254,802.58元、延迟履行违约金71,399.68元及诉讼费用。被告辩称，系争合同已终止，欠款金额应为499,908元，且不认可违约金。\n法院认为，原告与腾双公司签订的测试合同适用于原被告，原告提供的测试服务应得到被告支付。依照《中华人民共和国合同法》第六十条、第一百零九条,《中华人民共和国民事诉讼法》第六十四条第一款,《最高人民法院关于适用〈中华人民共和国民事诉讼法〉的解释》第九十条之规定判决被告支付原告检测费1,254,802.58元及违约金71,399.68元。'}

```
