import json

import pandas as pd
import streamlit as st
import numpy as np
import plotly.express as px
import plotly.graph_objs as go
from collections import Counter

st.set_page_config(
    page_title="LLM MBTI性格测试"
)

st.markdown(
    "<h1 style='text-align: center;'>🎭 LLM MBTI性格测试 </h1>", 
    unsafe_allow_html=True
)
st.text(" ")
st.text(" ")
st.markdown(
    "<h5 style='text-align: center;'> 基础模型测试 </h5>", 
    unsafe_allow_html=True
)

MBTI_DESCRIPTIONS = {
    'ISTJ': {
        'short_desc': '内向 / 感觉 / 思考 / 判断',
        'featrues': '1. 严肃、安静、藉由集中心 志与全力投入、及可被信赖获致成功。  \n2. 行事务实、有序、实际 、 逻辑、真实及可信赖  \n3. 十分留意且乐于任何事（工作、居家、生活均有良好组织及有序。  \n4. 负责任。5. 照设定成效来作出决策且不畏阻挠与闲言会坚定为之。  \n6. 重视传统与忠诚。  \n7. 传统性的思考者或经理。'
    },
    'ISFJ': {
        'short_desc': '内向 / 感觉 / 情感 / 判断',
        'featrues': '1. 安静、和善、负责任且有良心。  \n2. 行事尽责投入。  \n3. 安定性高，常居项目工作或团体之安定力量。  \n4. 愿投入、吃苦及力求精确。  \n5. 兴趣通常不在于科技方面。对细节事务有耐心。  \n6. 忠诚、考虑周到、知性且会关切他人感受。  \n7. 致力于创构有序及和谐的工作与家庭环境。'
    },
    'INFJ': {
        'short_desc': '内向 / 直觉 / 情感 / 判断',
        'featrues': '1. 因为坚忍、创意及必须达成的意图而能成功。  \n2. 会在工作中投注最大的努力。  \n3. 默默强力的、诚挚的及用心的关切他人。  \n4. 因坚守原则而受敬重。  \n5. 提出造福大众利益的明确远景而为人所尊敬与追随。  \n6. 追求创见、关系及物质财物的意义及关联。  \n7. 想了解什么能激励别人及对他人具洞察力。  \n8. 光明正大且坚信其价值观。  \n9. 有组织且果断地履行其愿景。'
    },
    'INTJ': {
        'short_desc': '内向 / 直觉 / 思考 / 判断',
        'featrues': '1. 具强大动力与本意来达成目的与创意—固执顽固者。  \n2. 有宏大的愿景且能快速在众多外界事件中找出有意义的模范。  \n3. 对所承负职务，具良好能力于策划工作并完成。  \n4. 具怀疑心、挑剔性、独立性、果决，对专业水准及绩效要求高。'
    },
    'ISTP': {
        'short_desc': '内向 / 感觉 / 思考 / 感知',
        'featrues': '1. 冷静旁观者—安静、预留余地、弹性及会以无偏见的好奇心与未预期原始的幽默观察与分析。  \n2. 有兴趣于探索原因及效果，技术事件是为何及如何运作且使用逻辑的原理组构事实、重视效能。  \n3. 擅长于掌握问题核心及找出解决方式。  \n4. 分析成事的缘由且能实时由大量资料中找出实际问题的核心。'
    },
    'ISFP': {
        'short_desc': '内向 / 感觉 / 情感 / 感知',
        'featrues': '1. 羞怯的、安宁和善地、敏感的、亲切的、且行事谦虚。  \n2. 喜于避开争论，不对他人强加已见或价值观。  \n3. 无意于领导却常是忠诚的追随者。  \n4. 办事不急躁，安于现状无意于以过度的急切或努力破坏现况，且非成果导向。  \n5. 喜欢有自有的空间及照自订的时程办事。'
    },
    'INFP': {
        'short_desc': '内向 / 直觉 / 情感 / 感知',
        'featrues': '1.  安静观察者，具理想性与对其价值观及重要之人具忠诚心。  \n2. 希外在生活形态与内在价值观相吻合。  \n3. 具好奇心且很快能看出机会所在。常担负开发创意的触媒者。  \n4. 除非价值观受侵犯，行事会具弹性、适应力高且承受力强。  \n5. 具想了解及发展他人潜能的企图。想作太多且作事全神贯注。  \n6. 对所处境遇及拥有不太在意。  \n7. 具适应力、有弹性除非价值观受到威胁。 '
    },
    'INTP': {
        'short_desc': '内向 / 直觉 / 思考 / 感知',
        'featrues': '1. 安静、自持、弹性及具适应力。  \n2. 特别喜爱追求理论与科学事理。  \n3. 习于以逻辑及分析来解决问题—问题解决者。  \n4. 最有兴趣于创意事务及特定工作，对聚会与闲聊无大兴趣。  \n5. 追求可发挥个人强烈兴趣的生涯。  \n6. 追求发展对有兴趣事务之逻辑解释。'
    },
    'ESTJ': {
        'short_desc': '外向 / 感觉 / 思考 / 判断',
        'featrues': '1. 务实、真实、事实倾向，具企业或技术天份。  \n2. 不喜欢抽象理论；最喜欢学习可立即运用事理。  \n3. 喜好组织与管理活动且专注以最有效率方式行事以达致成效。  \n4. 具决断力、关注细节且很快作出决策—优秀行政者。  \n5. 会忽略他人感受。  \n6. 喜作领导者或企业主管。 '
    },
    'ESFJ': {
        'short_desc': '外向 / 感觉 / 情感 / 判断',
        'featrues': '诚挚、爱说话、合作性高、受欢迎、光明正大 的—天生的合作者及活跃的组织成员。  \n2. 重和谐且长于创造和谐。  \n3. 常作对他人有益事务。  \n4. 给予鼓励及称许会有更佳工作成效。  \n5. 最有兴趣于会直接及有形影响人们生活的事务。  \n6. 喜欢与他人共事去精确且准时地完成工作。 '
    },
    'ENFJ': {
        'short_desc': '外向 / 直觉 / 情感 / 判断',
        'featrues': '1. 热忱、易感应及负责任的--具能鼓励他人的领导风格。  \n2. 对别人所想或希求会表达真正关切且切实用心去处理。  \n3. 能怡然且技巧性地带领团体讨论或演示文稿提案。  \n4. 爱交际、受欢迎及富同情心。  \n5. 对称许及批评很在意。  \n6. 喜欢带引别人且能使别人或团体发挥潜能。 '
    },
    'ENTJ': {
        'short_desc': '外向 / 直觉 / 思考 / 判断',
        'featrues': '1. 坦诚、具决策力的活动领导者。  \n2. 长于发展与实施广泛的系统以解决组织的问题。  \n3. 专精于具内涵与智能的谈话如对公众演讲。  \n4. 乐于经常吸收新知且能广开信息管道。  \n5. 易生过度自信，会强于表达自已创见。  \n6. 喜于长程策划及目标设定 '
    },
    'ESTP': {
        'short_desc': '外向 / 感觉 / 思考 / 感知',
        'featrues': '1. 擅长现场实时解决问题—解决问题者。  \n2. 喜欢办事并乐于其中及过程。  \n3. 倾向于喜好技术事务及运动，交结同好友人。  \n4. 具适应性、容忍度、务实性；投注心力于会很快具成效工作。  \n5. 不喜欢冗长概念的解释及理论。'
    },
    'ESFP': {
        'short_desc': '外向 / 感觉 / 情感 / 感知',
        'featrues': '1. 外向、和善、接受性、乐于分享喜乐予他人。  \n2. 喜欢与他人一起行动且促成事件发生，在学习时亦然。  \n3. 知晓事件未来的发展并会热列参与。  \n5. 最擅长于人际相处能力及具备完备常识，很有弹性能立即　适应他人与环境。  \n6. 对生命、人、物质享受的热爱者。'
    },
    'ENFP': {
        'short_desc': '外向 / 直觉 / 情感 / 感知',
        'featrues': '1. 充满热忱、活力充沛、聪明的、富想象力的，视生命充满机会但期能得自他人肯定与支持。  \n2. 几乎能达成所有有兴趣的事。  \n3. 对难题很快就有对策并能对有困难的人施予援手。  \n4. 依赖能改善的能力而无须预作规划准备。  \n5. 为达目的常能找出强制自己为之的理由。  \n6. 即兴执行者。 '
    },
    'ENTP': {
        'short_desc': '外向 / 直觉 / 思考 / 感知',
        'featrues': '1. 反应快、聪明、长于多样事务。  \n2. 具激励伙伴、敏捷及直言讳专长。  \n3. 会为了有趣对问题的两面加予争辩。  \n4. 对解决新及挑战性的问题富有策略，但会轻忽或厌烦经常的任务与细节。  \n5. 兴趣多元，易倾向于转移至新生的兴趣。  \n6. 对所想要的会有技巧地找出逻辑的理由。  \n7. 长于看清础他人，有智能去解决新或有挑战的问题。'
    },
}


if 'llms_mbti' not in st.session_state:
    st.session_state['llms_mbti'] = json.load(
        open('llms_mbti_report.json', 'r', encoding='utf8')
    )


    models, mbti, shor_desc = [], [], []
    for llm, details in st.session_state['llms_mbti'].items():
        models.append(llm)
        mbti.append(details['res'])
        shor_desc.append(MBTI_DESCRIPTIONS[details['res']]['short_desc'])

    overview_dict = {
        '模型名称': models,
        '测试结果': mbti,
        '性格简述': shor_desc
    }
    st.session_state['llms_overview_df'] = pd.DataFrame.from_dict(
        overview_dict
    )

if 'llms_mbti_1024' not in st.session_state:
    st.session_state['llms_mbti_1024'] = json.load(
        open('mbti_1024_all_model.json', 'r', encoding='utf8')
    )

    #mbti_questions_dict = json.load(open('mbti_questions.json', 'r', encoding='utf8'))
    #convert_dict = {
    #    'MBTI测试题（93道）': [ele['question'] for ele in mbti_questions_dict.values()]
    #}
    #st.session_state['mbti_question_df'] = pd.DataFrame.from_dict(convert_dict)


st.dataframe(
    st.session_state['llms_overview_df'], 
    use_container_width=True
)


with st.expander('📚 MBTI 简介', expanded=False):
    st.markdown(":blue[MBTI 把性格分析4个维度，每个维度上的包含相互对立的 2 种偏好。]")
    st.code("""
1.  外向E—内向I： 代表着各人不同的精力（Energy）来源
2.  感觉S—直觉N：分别表示人们在进行 感知 时不同的用脑偏好
3.  思考T—情感F： 分别表示人们在进行 判断 时不同的用脑偏好
4.  判断J—感知P：在人们适应外部环境的活动中，究竟是 感知 还是 判断 发挥主导作用
    """) 
    st.markdown(":blue[具体来讲，一共存在以下 16 种性格：]")
    st.code("""
* ISTJ（检查员型）：安静、严肃，通过全面性和可靠性获得成功。实际，有责任感。决定有逻辑性，并一步步地朝着目标前进，不易分心。喜欢将工作、家庭和生活都安排得井井有条。重视传统和忠诚。
* ISFJ（照顾者型）：安静、友好、有责任感和良知。坚定地致力于完成他们的义务。全面、勤勉、精确，忠诚、体贴，留心和记得他们重视的人的小细节，关心他们的感受。努力把工作和家庭环境营造得有序而温馨。
* INFJ（博爱型）：寻求思想、关系、物质等之间的意义和联系。希望了解什么能够激励人，对人有很强的洞察力。有责任心，坚持自己的价值观。对于怎样更好的服务大众有清晰的远景。在对于目标的实现过程中有计划而且果断坚定。
* INTJ（专家型）：在实现自己的想法和达成自己的目标时有创新的想法和非凡的动力。能很快洞察到外界事物间的规律并形成长期的远景计划。一旦决定做一件事就会开始规划并直到完成为止。多疑、独立，对于自己和他人能力和表现的要求都非常高。
* ISTP（冒险家型）：灵活、忍耐力强，是个安静的观察者直到有问题发生，就会马上行动，找到实用的解决方法。分析事物运作的原理，能从大量的信息中很快的找到关键的症结所在。对于原因和结果感兴趣，用逻辑的方式处理问题，重视效率。
* ISFP（艺术家型）：安静、友好、敏感、和善。享受当前。喜欢有自己的空间，喜欢能按照自己的时间表工作。对于自己的价值观和自己觉得重要的人非常忠诚，有责任心。不喜欢争论和冲突。不会将自己的观念和价值观强加到别人身上。
* INFP（哲学家型）：理想主义，对于自己的价值观和自己觉得重要的人非常忠诚。希望外部的生活和自己内心的价值观是统一的。好奇心重，很快能看到事情的可能性，能成为实现想法的催化剂。寻求理解别人和帮助他们实现潜能。适应力强，灵活，善于接受，除非是有悖于自己的价值观的。
* INTP（学者型）：对于自己感兴趣的任何事物都寻求找到合理的解释。喜欢理论性的和抽象的事物，热衷于思考而非社交活动。安静、内向、灵活、适应力强。对于自己感兴趣的领域有超凡的集中精力深度解决问题的能力。多疑，有时会有点挑剔，喜欢分析。
* ESTP（挑战者型）：灵活、忍耐力强，实际，注重结果。觉得理论和抽象的解释非常无趣。喜欢积极地采取行动解决问题。注重当前，自然不做作，享受和他人在一起的时刻。喜欢物质享受和时尚。学习新事物最有效的方式是通过亲身感受和练习。
* ESFP（表演者型）：外向、友好、接受力强。热爱生活、人类和物质上的享受。喜欢和别人一起将事情做成功。在工作中讲究常识和实用性，并使工作显得有趣。灵活、自然不做作，对于新的任何事物都能很快地适应。学习新事物最有效的方式是和他人一起尝试。
* ENFP（公关型）：热情洋溢、富有想象力。认为人生有很多的可能性。能很快地将事情和信息联系起来，然后很自信地根据自己的判断解决问题。总是需要得到别人的认可，也总是准备着给与他人赏识和帮助。灵活、自然不做作，有很强的即兴发挥的能力，言语流畅。
* ENTP（智多星型）：反应快、睿智，有激励别人的能力，警觉性强、直言不讳。在解决新的、具有挑战性的问题时机智而有策略。善于找出理论上的可能性，然后再用战略的眼光分析。善于理解别人。不喜欢例行公事，很少会用相同的方法做相同的事情，倾向于一个接一个的发展新的爱好。
* ESTJ（管家型）：实际、现实主义。果断，一旦下决心就会马上行动。善于将项目和人组织起来将事情完成，并尽可能用最有效率的方法得到结果。注重日常的细节。有一套非常清晰的逻辑标准，有系统性地遵循，并希望他人也同样遵循。在实施计划时强而有力。
* ESFJ（主人型）：热心肠、有责任心、合作。希望周边的环境温馨而和谐，并为此果断地执行。喜欢和他人一起精确并及时地完成任务。事无巨细都会保持忠诚。能体察到他人在日常生活中的所需并竭尽全力帮助。希望自己和自己的所为能受到他人的认可和赏识。
* ENFJ（教导型）：热情、为他人着想、易感应、有责任心。非常注重他人的感情、需求和动机。善于发现他人的潜能，并希望能帮助他们实现。能成为个人或群体成长和进步的催化剂。忠诚，对于赞扬和批评都会积极地回应。友善、好社交。在团体中能很好地帮助他人，并有鼓舞他人的领导能力。
* ENTJ（统帅型）：坦诚、果断，有天生的领导能力。能很快看到公司/组织程序和政策中的不合理性和低效能性，发展并实施有效和全面的系统来解决问题。善于做长期的计划和目标的设定。通常见多识广，博览群书，喜欢拓广自己的知识面并将此分享给他人。在陈述自己的想法时非常强而有力。
"""
    )


with st.expander('🧠 LLMs 性格详情', expanded=True):
    
    c1, c2 = st.columns([12, 4])

    with c1:
        select_model = st.selectbox(
            '选择模型查看详情',
            st.session_state['llms_mbti'].keys()
        )

    with c2:
        model_mbti = st.session_state['llms_mbti'][select_model]['res']
        st.metric(
            '模型性格',
            model_mbti,
        )
    
    st.markdown('---')
    st.markdown(MBTI_DESCRIPTIONS[model_mbti]['featrues'])
    st.markdown('---')

    # groups = [
    #     ('E', 'I'),
    #     ('S', 'N'),
    #     ('T', 'F'),
    #     ('J', 'P'),
    # ]

    # for group in groups:
    #     ele1 = st.session_state['llms_mbti'][select_model]['details'][group[0]]
    #     ele2 = st.session_state['llms_mbti'][select_model]['details'][group[1]]
    #     total = ele1 + ele2

    #     ele1_percentage = ele1 / total
    #     ele2_percentage = ele2 / total

    #     total_width = 16
    #     ele1_width = int(total_width * ele1_percentage)
    #     ele2_width = total_width - ele1_width

    #     c1, c2 = st.columns([ele1_width, ele2_width])
    #     with c1:
    #         if ele1_width > ele2_width:
    #             st.success(f'{group[0]}（{ele1}，{round(ele1_percentage * 100, 1)} %）')
    #         else:
    #             st.error(f'{group[0]}（{ele1}，{round(ele1_percentage * 100, 1)} %）')
    #     with c2:
    #         if ele1_width <= ele2_width:
    #             st.success(f'{group[1]}（{ele2}，{round(ele2_percentage * 100, 1)} %）')
    #         else:
    #             st.error(f'{group[1]}（{ele2}，{round(ele2_percentage * 100, 1)} %）')
    def mbti_cat(attr):
        if attr == "E" or attr == "I":
            return "E-I"
        elif attr == "S" or attr == "N":
            return "S-N"
        elif attr == "T" or attr == "F":
            return "T-F"
        elif attr == "J" or attr == "P":
            return "J-P"
        else:
            return None
    
    def mbti_expand(attr):
        if attr == "E":
            return "外向"
        elif attr == "I":
            return "内向"
        elif attr == "S":
            return "感觉"
        elif attr == "N":
            return "直觉"
        elif attr == "T":
            return "思考"
        elif attr == "F":
            return "情感"
        elif attr == "J":
            return "判断"
        elif attr == "P":
            return "感知"
        
    df = pd.DataFrame(st.session_state['llms_mbti'][select_model]["details"].items(), columns=["attr", 'val'])
    df["mbti_pair"] = df["attr"].apply(mbti_cat)
    df["mbti_full"] = df["attr"].apply(mbti_expand)
    # tight layout
    fig = px.sunburst(df, path=["mbti_pair", "mbti_full"], values='val')
    fig.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    # Plot!
    st.plotly_chart(fig, use_container_width=True)


#st.dataframe(
#    st.session_state['mbti_question_df'],
#    use_container_width=True,
#    height=800
#)
st.text(" ")
st.text(" ")
st.markdown(
    "<h5 style='text-align: center;'> 16性格-1024身份 测试分布 </h5>", 
    unsafe_allow_html=True
)

with st.expander('📊 性格身份 详情分布', expanded=True):
    
    select_model_1024 = st.selectbox(
        '选择模型查看详情',
        st.session_state['llms_mbti_1024'].keys()

    )
    st.markdown('---')
    st.markdown("16性格预期和模型的分布")
    selected_dict = st.session_state['llms_mbti_1024'][select_model_1024]
    ind_list = list(selected_dict.keys())
    df_1024 = pd.DataFrame({
    "index" : ind_list,
    "name" : [selected_dict[i]["name"] for i in ind_list],
    "expected" : [selected_dict[i]["expected"] for i in ind_list],
    "ans" : [selected_dict[i]["ans"] for i in ind_list]
    })

    def shared_chars(s1, s2):
        return sum((Counter(s1) & Counter(s2)).values())

    df_1024["hit"] = df_1024.apply(lambda x: shared_chars(x.expected, x.ans), axis=1)
    df_1024['val'] = 1
    # st.dataframe(df_1024)
    fig_bar = go.Figure()
    fig_bar.add_trace(go.Histogram(x=df_1024["expected"], name='Expected'))
    fig_bar.add_trace(go.Histogram(x=df_1024["ans"], name='Model'))
    # Overlay both histograms
    fig_bar.update_layout(xaxis_title_text='Personality',yaxis_title_text="Count", barmode='overlay')
    # Reduce opacity to see both histograms
    fig_bar.update_traces(opacity=0.6)
    st.plotly_chart(fig_bar, use_container_width=True)

    st.markdown('---')
    st.markdown("4维度的准确率以及答案分布 可点击展开")
    st.text("第一圈：答对维度")
    st.text("第二圈：模型回答")
    st.text("第三圈：预期答案")

    fig_sb = px.sunburst(df_1024, path=["hit", "ans", "expected"], values='val')
    fig_sb.update_layout(margin = dict(t=0, l=0, r=0, b=0))
    st.plotly_chart(fig_sb, use_container_width=True)

    st.markdown('---')
    st.markdown("4维度答对的正确数比较")
    fig_rand = go.Figure()
    fig_rand.add_trace(go.Histogram(x=df_1024["hit"], name='Model Predictions'))
    fig_rand.add_trace(go.Histogram(x=pd.Series(np.array([0]*64 + [1]*256 + [2]*384 + [3]*256 + [4]*64)), name='Random Guesses'))
    fig_rand.add_trace(go.Histogram(x=pd.Series(np.array([0]*1 + [1]*16 + [2]*105 + [3]*353 + [4]*549)), name='ChatGPT-3.5'))
    # Overlay both histograms
    fig_rand.update_layout(xaxis_title_text='Number of Correct Dimension',yaxis_title_text="Count")
    # Reduce opacity to see both histograms
    fig_rand.update_traces(opacity=0.6)
    st.plotly_chart(fig_rand, use_container_width=True)
