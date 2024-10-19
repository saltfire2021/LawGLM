from knowledge.tools2json import TOOLS

# 在这里定义的k，v会根据正则匹配，加入 planer 的 tips
TIPS = {
    # '整合报告': '找到参数的dict_list中需要的信息然后传入/save_dict_list_to_word接口，注意哪些字段是不要的',
    "高消费.*审理法院|执行法院": "注意审理法院和执行法院不一样，限制高消费接口返回的是执行法院，需要通过案号获取审理法院",
    "律.{0,3}所.?负责人": "需要先找到律师事务所名称 然后/get_lawfirm_info接口查询LawfirmInfo",
    "在.{2,5}涉诉": '案号格式为 “(”+收案年度+“)”+法院代字+类型代字+案件编号+“号” ，统计在哪里涉诉，即统计案号中法院代字有没有这个省的简称 如在安徽涉诉即 "皖" in 案号',
    "不规则案号": "案号格式为 “(”+收案年度+“)”+法院代字+类型代字+案件编号+“号”,以下是一个标准案号：(2020)皖01民终1783号，其中(2020)表示2020年立案，皖01为法院代字，民终表示民事终审，1783号为案件编号",
    # '高新.*区县': '备注，诸如高新开发区，高新区，不是区县，应该基于这个地址查找所在区县',
    "[0-9A-Z]{18}": "统一社会信用代码查询公司名称的接口为：/get_company_register_name",
    # '立案日期|起诉日期': "立案日期 起诉日期 都是案号里的年份",
    # '审理日期': '审理日期是裁判文书里的日期也就是裁判文书表的日期字段',
    # '法人': '法人需要你从CompanyInfo获取法人代表 然后从CompanyRegister获取法定代表人 这两个字段，进行对比',
    "母公司": "用户给的有可能是子公司，并且需求母公司，需要找到其母公司",
    # '写一份': '写作需求实际是要你查询到所有的信息然后调用写作接口，特别的：【公司法人属于公民，公司法人起诉公司的关系为公民起诉公司】，你在思考的第一步是：区分起诉和被起诉的是公民还是公司，最后应该调用哪个写作接口，切记一定要使用接口写作',
    "公司代码": "公司代码需要使用 /get_company_info 转为公司名称",
    "度|天气": "如果题目需要查询温度，则需要日期和省市，请不要忘记查询日期",
    "案号.+法院|法院.+案号|[^执限].+法院": "如果不知道法院名称，你可以通过案号使用get_court_code_by_case_number获取法院名称，LegalDoc没有“审理法院”字段，如果已知晓法院名称或者查询的是限制高消费表，忽略此建议",
    "被投资|被控股": "被投资，被控股的一般是子公司，SubCompanyInfo表格可以获取此公司的母公司。",
    "原告|被告": "你可能需要使用 filter_legal_docs 函数过滤原告被告，注意获取案号的时候要添加原/被告字段",
    "位小数|亿": "你需要设置单独的步骤转化，其中只有注册资本单位为万元，注册资本转为亿元除以10000，其余金额如涉案金额单位为元",
    r"金额(?!.*(位小数|亿))": "只有注册资本单位为万元，其余金额如涉案金额单位为元",
    "[四4]位小数": "如果没有特殊说明，保留四位小数的意思是化为万元为单位",
    "省份|城市|区县": "省份|城市|区县需要通过具体地址调用/get_address_info获得",
    "受理费": "受理费用在判决结果内。",
    "胜诉|败诉|胜率|获胜": "获取胜诉方，败诉方，案件受理费用在判决结果，你应该在代码里打印出胜诉方是“原告”还是“被告”， 无法使用辅助函数过滤胜诉方和败诉方 胜诉/败诉方律师事务所在确定胜诉方之后直接使用 原告/被告律师事务所字段获得",
    "判决结果|案件.{0,3}费用": "案件受理费用在判决结果里",
    "公司简称": "公司简称需要使用接口转为公司全称进行接下来的查询过滤等操作(如果有)",
    "级别.{0,5}法院|法院.{0,5}级别": "如果获取最高审理级别法院可以使用sort_court_level可以进行排序，获取审理法院级别直接从接口获取",
    "行政级别": "法院行政级别从高到低为 省级>市级>区县级，获取行政级别最高的法院，你可以先进行数字映射然后排序，并打印排序结果，以上要在“suggestion”字段提示",
    "为法院代字": "法院代字你可以使用 /get_court_code 获取法院名称进行之后的查询",
    "邮箱地址": "邮箱地址为邮箱和地址",
    "组织机构.{0,3}码": "注意组织机构代码不是统一社会信用代码，可以直接使用公司全称查询",
    "(基层|中级|高级).{0,2}法院": "基层|中级|高级法院可以使用案号+get_court_code_by_case_number函数获取法院级别==基层|中级|高级法院",
    "律师事务所": "注意不要忘记获取原被告律师事务所，如果是判断雇佣选择的律师事务所，注意当事方是原告还是被告，这都有可能，查询包含原被告以及律师事务所，if 关联公司 in 原告 取原告律师事务所 反之取被告 (如果不是雇佣事务所忽略此条)",
    "法院名称.*案": "如果你需要筛选由某法院审理的案件需要使用案号循环调用 get_court_code_by_case_number 获取法院名称然后比较，如果有其他过滤条件，应该先进行其他条件的过滤，最后过滤法院名称",
    # '胜诉|败诉|判决结果|案件.{0,3}费用': '获取胜诉方，败诉方，案件受理费用需要使用自然语言进行判断判决结果，此步骤应该尽可能多判断，例如需要判断胜诉方律师事务所，你应该直接获取事务所，而不是胜诉方。你需要在规划json里把"type"字段变为"自然语言推理",此类型"suggestion"字段要更加详细',
    # '不规则案号|法院名称.*案号|案号.*法院名称': '案号格式为 “(”+收案年度+“)”+法院代字+类型代字+案件编号+“号”，你需要将不规则案号转为格式正确的案号，如果没有法院代字，根据法院名称，使用 /get_court_code 获取法院代字，不要使用get_court_code_by_case_number',
    "投资的.资公司": "用户可能需要的是全资子公司",
    "执.*申请人": "申请人和被申请人指的是限制高消费",
    "[^执].*申请人": "申请人是原告被申请人是被告",
    "由.*法院.*审": "由xxx法院审理通过法院代字过滤",
    "多少家子公司|几家子公司": "需要列举符合条件的子公司",
    # '[^执高].*法院':''
    # '案号.+法院':'get_court_code_by_case_number可以获取法院名称'
}


ERROR_TIPS = [
    {
        "pos_route": ["/get_legal_document", "/get_legal_abstract", "/get_xzgxf_info"],
        "pattern": "案号",
        "use_field": ["requirement", "param"],
        "content": "案号各基本要素的编排规格为：“(”+收案年度+“)”+法院代字+类型代字+案件编号+“号”。每个案件编定的案号均应具有唯一性。 其中年份的括号可以是中英文 都要尝试一遍，如果你没有法院代字，并且题目中有法院名称，通过 /get_court_code 接口获取法院代字，以下是一个标准案号：(2020)苏01民终1783号，其中(2020)表示2020年立案，苏01为法院代字，民终表示民事终审，1783号为案件编号",
    },
    {
        "pos_route": "ALL",
        "pattern": "母公司|子公司",
        "use_field": ["requirement", "param"],
        "content": "请确定公司是母公司还是子公司，如果是子公司，需要先获取母公司再去查询",
    },
    {
        "pos_route": "ALL",
        "pattern": "高新.*区县|区县代码",
        "use_field": ["requirement", "param"],
        "content": "备注，诸如高新开发区，高新区，不是区县，应该基于这个地址查找所在区县，另外，查找地址应该包含省市区，如果接口/get_address_info无法识别地址，你可以自行基于用户输入判断省市区，特别的如果是高新区你要基于自己的知识判断这个城市的高新区在哪，例如合肥市高新区你需要回答合肥市蜀山区，连云港高新区为海州区",
    },
    {
        "pos_route": "ALL",
        "pattern": "在.{2,5}涉诉",
        "use_field": ["requirement", "param"],
        "content": '案号格式为 “(”+收案年度+“)”+法院代字+类型代字+案件编号+“号” ，统计在哪里涉诉，即统计案号中法院代字有没有这个省的简称 如在安徽涉诉即 "皖" in 案号',
    },
    {
        "pos_route": [
            "/get_company_info",
            "/get_company_register",
            "/get_sub_company_info",
            "/get_sub_company_info_list",
            "/get_xzgxf_info_list",
            "/get_legal_document_list",
        ],
        "pattern": "[省市区]",
        "use_field": ["param"],
        "content": "公司名一般为 行政区划+字号+行业+组织形式组成，行政区划是名称如 “安徽”， “北京” 特别注意的是 没有 : “省”和“市” 去掉省市后重新查询,例如 北京市三元食品股份有限公司->北京三元食品股份有限公司",
    },
    {
        "pos_route": [
            "/get_company_info",
            "/get_company_register",
            "/get_sub_company_info",
            "/get_sub_company_info_list",
            "/get_xzgxf_info_list",
            "/get_legal_document_list",
        ],
        "pattern": "^(?!.*(省|市|区)).*[$\n]",
        "use_field": ["requirement", "param"],
        "content": "请确定公司名有没有拼写错误，例如重复打字，公司名一般为 行政区划+字号+行业+组织形式组成，如果是集团，一般名字是公司的简称+集团股份有限公司，例如：龙元建设集团股份有限公司,如果你不是很确定，你可以从公司名称中找到公司简称，然后通过/get_company_info 传入 {'query_conds':{'公司简称':'str'},'need_fields':['公司名称']} 获取正确的公司名称，如果历史记录中有纠正后的公司名称，你可以从历史记录里找到正确的名称，请先看有没有历史记录，然后尝试修复名称，最后尝试简称，，另外，也要检查省市名称是否正确，例如温洲->温州",
    },
    {
        "pos_route": ["/get_court_code"],
        "pattern": ".",
        "use_field": ["requirement", "param"],
        "content": "法院或者法院代字未录入，请检查输入是否正确",
    },
    {
        "pos_route": ["/get_legal_document"],
        "pattern": "执",
        "use_field": ["requirement", "param"],
        "content": "执行案件可以尝试查询 /get_xzgxf_info 获取结果",
    },
    {
        "pos_route": ["/get_court_info", "/get_court_code"],
        "pattern": "法院",
        "use_field": ["requirement", "param"],
        "content": "法院名一般为 所在地+级别+法院类型,所在地为xxx省xxx市xxx区/县等 其中省市区县几个字不能省略，表示所在地，但是可以没有市区县，表示省级法院，同理，也有市级别,例如：福建省漳州市中级人民法院",
    },
    {
        "pos_route": "ALL",
        "pattern": "统一社会信用代码|组织机构代码",
        "use_field": ["requirement", "param"],
        "content": '统一社会信用代码 只能 在/get_company_register_name 中使用 {"query_conds": {"统一社会信用代码": "xxx"}, "need_fields": []} 方式使用',
    },
    {
        "pos_route": "ALL",
        "pattern": r"(?<!\d)\d{7,12}(?!\d)",
        "use_field": ["requirement", "param"],
        "content": "如果与公司相关，可能是错误的公司代码，建议检查有没有重复数字，推荐转成6位数字转成公司代码，使用for [所有的可能（一般300 600开头）] 找到正确的",
    },
    {
        "pos_route": ["/get_address_info"],
        "pattern": ".",
        "use_field": ["requirement", "param"],
        "content": "API info: /get_address_info 调用失败，请你自行从地址中获取省,市,区，备注:高新区不算区，你需要按照自己的知识进行判断，例如合肥市高新区你需要回答合肥市蜀山区。请你判断后赋值，打印。",
    },
    {
        "pos_route": ["/get_lawfirm_info", "/get_lawfirm_log"],
        "pattern": ".",
        "use_field": ["requirement", "param"],
        "content": "API info: /get_lawfirm_info 调用失败，应该传入的是律师事务所名称，你可以从之前的内容直接判断需要传入的律师事务所名称，直接构造参数，不要使用之前的ipython缓存。",
    },
    {
        "pos_route": ["/get_temp_info"],
        "pattern": ".",
        "use_field": ["requirement", "param"],
        "content": 'API info: 没有查询到天气信息，请确保省市名称完整，不要省略省、市字样，你可以基于历史自己填入信息，无需使用代码拼凑，日期使用示例的格式，不要有汉字 参数示例为{"query_conds": {"省份": "北京市", "城市": "北京市", "日期": "2020年1月1日"}, "need_fields": []}',
    },
    {
        "pos_route": ["/get_citizens_sue_citizens"],
        "pattern": ".",
        "use_field": [],
        "content": "API info: /get_citizens_sue_citizens调用失败，请你按照{'原告': '张三', '原告性别': '男', '原告生日': '1976-10-2', '原告民族': '汉', '原告工作单位': 'XXX', '原告地址': '中国', '原告联系方式': '123456', '原告委托诉讼代理人': '李四', '原告委托诉讼代理人联系方式': '421313', '被告': '王五', '被告性别': '女', '被告生日': '1975-02-12', '被告民族': '汉', '被告工作单位': 'YYY', '被告地址': '江苏', '被告联系方式': '56354321', '被告委托诉讼代理人': '赵六', '被告委托诉讼代理人联系方式': '09765213', '诉讼请求': 'AA纠纷', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '最高法', '起诉日期': '2012-09-08'} 的格式，手动书写参数并调用",
    },
    {
        "pos_route": ["/get_company_sue_citizens"],
        "pattern": ".",
        "use_field": [],
        "content": "API info: /get_company_sue_citizens调用失败，请你按照{'原告': '上海公司', '原告地址': '上海', '原告法定代表人': '张三', '原告联系方式': '872638', '原告委托诉讼代理人': 'B律师事务所', '原告委托诉讼代理人联系方式': '5678900', '被告': '王五', '被告性别': '女', '被告生日': '1975-02-12', '被告民族': '汉', '被告工作单位': 'YYY', '被告地址': '江苏', '被告联系方式': '56354321', '被告委托诉讼代理人': '赵六', '被告委托诉讼代理人联系方式': '09765213', '诉讼请求': 'AA纠纷', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '最高法', '起诉日期': '2012-09-08'} 的格式，手动书写参数并调用",
    },
    {
        "pos_route": ["/get_citizens_sue_company"],
        "pattern": ".",
        "use_field": [],
        "content": "API info: /get_citizens_sue_company调用失败，请你按照{'原告': '张三', '原告性别': '男', '原告生日': '1976-10-2', '原告民族': '汉', '原告工作单位': 'XXX', '原告地址': '中国', '原告联系方式': '123456', '原告委托诉讼代理人': '李四', '原告委托诉讼代理人联系方式': '421313', '被告': '王五公司', '被告地址': '公司地址', '被告法定代表人': '赵四', '被告联系方式': '98766543', '被告委托诉讼代理人': 'C律师事务所', '被告委托诉讼代理人联系方式': '425673398', '诉讼请求': 'AA纠纷', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '最高法', '起诉日期': '2012-09-08'} 的格式，手动书写参数并调用",
    },
    {
        "pos_route": ["/get_company_sue_company"],
        "pattern": ".",
        "use_field": [],
        "content": "API info: /get_company_sue_company调用失败，请你按照{'原告': '上海公司', '原告地址': '上海', '原告法定代表人': '张三', '原告联系方式': '872638', '原告委托诉讼代理人': 'B律师事务所', '原告委托诉讼代理人联系方式': '5678900', '被告': '王五公司', '被告地址': '公司地址', '被告法定代表人': '赵四', '被告联系方式': '98766543', '被告委托诉讼代理人': 'C律师事务所', '被告委托诉讼代理人联系方式': '425673398', '诉讼请求': 'AA纠纷', '事实和理由': '上诉', '证据': 'PPPPP', '法院名称': '最高法', '起诉日期': '2012-09-08'} 的格式，手动书写参数并调用",
    },
]
