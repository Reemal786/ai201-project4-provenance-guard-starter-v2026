
"""
Evaluation scenarios for Provenance Guard — Unit 8, Milestone 3.

Criteria:
1. Human-writing false positives
2. Human vs. AI combined-score separation
3. All three labels are reachable
4. Appeals (tested separately because run_eval.py only calls /submit)
5. Invalid-input handling

Each scenario is executed three times by run_eval.py.
"""

# Original writing supplied by the project author.
# Preserve the original wording for an authentic human-writing evaluation.

HUMAN_TEXTS = [
    """My passion for healthcare started from my formative experience at High School for Health Professions & Human Services, where I not only completed a medical assistant training program and but also conducted a literature review on African Sleeping Sickness, Cardiac Surgery, and Dengue in the Indian Subcontinent. Through my research I learned how cutting-edge technology was being used in diagnosing and treating these conditions. This led to my interest in using my medical knowledge along with my passion for technology to help improve patient outcomes.""",

    """Despite all the positive effects, the 2020 census is at risk. This risk includes the addition of a citizenship question in the census which would result in the ever-growing distrust in the federal government. Commerce Secretary Wilbur Ross announced that he informed the Census Bureau to ask respondents of the upcoming census in 2020 of their citizenship statuses. Regardless of numerous objections from former census directors, Republic and Democratic mayors, attorney generals, and civil rights organizations, Secretary Ross has still decided to include the question. The stakes of including such a question would result in the inadequate picture of the American population. A citizenship question has not been included since 1950. Regardless of what politicians who are in favor of the question state the Constitution is very clear. The significance of the census is to determine how many people live in a household and how many households reside in that specific area which would determine the number of representatives given to that country. The constitution, however, does not state how many of those census respondents hold citizenship. America was built due to the hard work of immigrants, immigrants who weren’t all granted citizenship. A citizenship question is a strike on our representative democracy and the inclusion of such a question is strictly political, as stated by former U.S. Attorney General Eric H. Holder Jr. Adding a citizenship question would significantly reduce census participation both by citizens and non-citizens not to mention increasing the fears of undocumented individuals that their responses may be used against them.""",

    """The first step in analyzing data and creating visualizations is data cleaning. For our project, we acquired data from three different sources with three different levels of standardization: median household income for families in NYC standardized by community districts, COVID-19 cases in New York City standardized by zip codes, and rental inventory data standardized by neighborhoods. Before beginning the process of data cleaning, we needed to decide on a certain geo-organization level by which to organize the data. We concluded organizing the date based on community districts. The benefit of this organization is that it would allow for the comparison of data based on a common point, the community district. One of the major disadvantages of this is the loss of detail in the data. This loss of detail occurs because organization based on community district is broader than organization by zip codes or neighborhoods. Although the loss of detail has implications on our findings, we were unable to acquire median household income data based on zip codes or neighborhoods. Furthermore, reformatting median household income data to organize it by neighborhoods or zip codes would not provide an accurate representation of the data.""",

    """The act of refusing to learn anything especially work taught in school has never been heard of. Until I came across Herbert Kohls “I won’t learn from you”. In this excerpt, Herbert recalls three different students with both different economical and social backgrounds who refused to take part in leaning the fundamentals taught in Herbert’s class. Out of all three of the youngsters, Akmir, Barry, and Rick I’ve shown a keen interest in Ricks refusal to learn. What sparked an interest in me about Rick was that the reason he refused to learn was not because he didn’t have the ability to learn, quite the contrary, but because he didn’t agree against the idea of students being tests and measured against each other. For instance, Rick recalls that the hardest thing that he had to not learn was algebra. Although he refused to learn, he believed that algebra could have be as interesting to him as chess was. As stated by “I won’t learn from you”, “In order to force failure [in algebra] Rick found ingenious ways to dissolve equations into marks on the page by creating visual exercises.” Algebra wasn’t like any other subject’s Rick refused to learn because refusing algebra was just as hard as trying to learn. Reading Ricks story made me realize that I have something in common with him. Although there are times where I have refused to learn, what I believe to be the most common similarity is his belief that the world has been pulled part by greed and competition which is one of the reasons why he began his band after dropping out. Although I might share this common belief the ability to refuse to learn and get away with it seems so bizarre. I cannot imagine a life full of success and freedom without some sort of education. I believe that in the world that we leave in today education is such an important part of our life granted we spend most of it trying to achieve any sort of recognition or attention""",

    """The consumption of sugar has become a part of our daily routine, from the snicker bars we eat to the beverages we buy at the end of our day. Over the past few years, the sugar intake of Americans has dramatically increased causing concern for organizations such as the US Food and Drug Administration (FDA). With this knowledge, the question about whether to regulate the amount of sugar added in soda and other sweetened beverages in order to reverse the effects of such a high intake has brought up several conflicting viewpoints. However, sugar intake should be restricted in order to prevent dangerous consequences such as deadly diseases, addiction and similar effects of alcohol.""",

    """With assests worth $5 trilion, BlackRock is one of the largest corporations in the world dedicated to offering a variety of investment solutions.creating two gun free investment funds and support organizations that would force Sturm Ruger, an American firearm manufatoring company, to create a report explaining the risks posed by the companies activites which in turn would promote grater gun safety. Showing leadership on environmental, social and governance matters, The Interfaith Center on Corporate Responsibility commneds the companys revolutionary succes, stating that it “Sends a strong message to Sturm Ruger’s board that business as usual is insufficient given the current climate, and that new safety standards responding to the risks guns pose for society are needed. “ althouhg this is a right step toward minimizing gun violence and encouraging other compnaies to consider the dmage of their work on society, BlackRock falls quite short when it comes to violnce impacted on a more global level.""",

    """According to Lockheed Martin, their nuclear weapons and control systems can be found on all U.S. Navy nuclear submarines and aircraft carriers stationed worldwide. Lockheed Martin produces a wide variety of nuclear weapons. For instance, the Trident 2 D5 nuclear missiles are found on U.S. Ohio-class and British Vanguard-class submarines. Lockheed is a part of AWE (Atomic Weapons Establishment), which manages the UK nuclear warhead system, Trident. The US Department of Defense currently budgets 561 Trident 2 missiles, worth $65 million each. Excluding research and development costs, $35 billion has been put into acquiring these missiles; one can only dream how much it would cost including research and development. At the price of $452 million, Lockheed Martin has been contracted to maintain and develop the Minuteman 3 missile system.""",

    """The Rise of Islam had a positive impact on the world because it promoted equality, sparked many life changing achievements, increased trade and boosted the economy. Islam preached one god, this meant as long as there was one god there was one people. Additionally, achievements in places such as trigonometry, astronomy, and algebra are all still used today and are imbedded in our daily lives. Innovations in engineering and medicine paved way for future accomplishments, ideas and saved hundreds of lives. The Islamic empire created their own alphabet and writing style, which can be observed in the Quran. Advancements in architecture and the arts were also made which are still seen today. Trade in Mecca thrived and the demand of goods increased.""",

    """African Sleeping Sickness, also known as Human African Trypanosomiasis is a vector borne parasitic disease. A vector borne disease is a disease that results from transferred to humans or other animals via blood feeding arthropods, such as mosquitos, ticks and/or fleas. African Sleeping Sickness is caused by an infection with protozoan parasites which belong to the genus, subfamily, Trypanosoma. Then, the parasites are transmitted by Glossina genus also known as tsetse fly. These flies acquire the infection from humans or animals that are harboring the pathogenic parasites. Found in sub-Saharan Africa, only a certain species of Tsetse flies can transmit the disease to victims who could further transfers the disease. Surprisingly, in many regions where tsetse flies are found sleeping sickness is not. Populations residing in the countryside where transmissions occur and who depend on agriculture, fishing, animal cultivation and/or hunting are the most exposed to the tsetse fly and therefore to the disease. Ranging from single small villages to and entire region, the intensity of the disease can vary from one village to the next within an infected area.""",

    """West African Trypanosomiasis, also known as Gambian sleeping sickness, is caused by the Trypanosoma Brucei Gambiense parasite carried by tsetse flies. Found in 24 countries in West and Central Africa, Trypanosoma Brucei Gambiense has currently 97% reported cases of sleeping sickness including causes of chronic infection. Infections can last for several months or years without major signs or symptoms of the disease. When symptoms emerge, the patient is often at an advanced stage where the central nervous system is affected. As mentioned before, tsetse flies that transmit West African Trypanosomiasis are found only in rural areas; therefore, travelers to urban areas are not at risk. Inhabiting forests and areas of thick vegetation along water, the flies bite during daylight hours. Where Gambian sleeping sickness is present, most flies are not infected with the parasite; therefore, the level of infection increases with the number of bites a person receives from the tsetse fly. Consequently, tourists who don’t spend long periods of time in rural areas of central Africa where the disease is present are at a low risk of obtaining said disease.""",
]

# AI-generated writing produced specifically for this evaluation.

AI_TEXTS = [
    """Artificial intelligence is transforming the healthcare industry by enabling medical professionals to analyze large volumes of patient information more efficiently. Machine learning algorithms can identify patterns in medical images, assist in predicting disease progression, and support clinical decision-making. These technologies have the potential to improve diagnostic accuracy and reduce the administrative burden on healthcare workers. However, the implementation of artificial intelligence also introduces challenges involving patient privacy, algorithmic bias, and transparency. Healthcare organizations must carefully evaluate these concerns to ensure that technological advancements benefit patients without compromising the quality and fairness of medical care.""",

    """Renewable energy technologies play an increasingly important role in addressing global environmental challenges. Solar panels, wind turbines, and hydroelectric systems generate electricity using naturally replenished resources, reducing dependence on fossil fuels. Although renewable energy offers substantial environmental benefits, its widespread adoption requires improvements in energy storage, electrical infrastructure, and manufacturing efficiency. Governments and private organizations can accelerate this transition through investments in research, infrastructure development, and sustainable energy policies. A balanced approach that considers economic feasibility, environmental protection, and technological innovation is essential for establishing reliable energy systems.""",

    """Cybersecurity has become an essential consideration for organizations that rely on digital infrastructure. As businesses increasingly store sensitive information in cloud environments, protecting data against unauthorized access and malicious attacks is critically important. Effective cybersecurity strategies combine technical safeguards, employee education, and continuous system monitoring. Encryption protects confidential information, while multifactor authentication reduces the likelihood of unauthorized account access. Regular security assessments can also identify vulnerabilities before attackers exploit them. Ultimately, cybersecurity requires ongoing adaptation because emerging technologies and evolving threats continuously introduce new risks.""",

    """Public transportation systems contribute significantly to the economic and environmental sustainability of urban communities. Reliable buses, trains, and subway networks provide residents with affordable access to employment, education, and essential services. By reducing dependence on personal vehicles, public transportation can help decrease traffic congestion and greenhouse gas emissions. Nevertheless, transportation agencies frequently encounter challenges involving aging infrastructure, maintenance expenses, and uneven service availability. Strategic investments in accessibility, reliability, and network expansion can improve transportation outcomes while supporting broader goals related to urban development and social equity.""",

    """Technology has changed how students access information, communicate with instructors, and complete academic assignments. Online learning platforms provide opportunities for flexible instruction, allowing students to review educational materials according to their individual schedules. Interactive applications can also support personalized learning by adapting activities to different levels of understanding. Despite these advantages, unequal access to reliable internet connections and digital devices may reinforce existing educational disparities. Educational institutions should therefore approach technological integration thoughtfully, ensuring that digital resources complement effective teaching practices rather than replacing meaningful interaction between students and educators.""",

    """Industrial robots are widely used in manufacturing environments to perform repetitive tasks with speed, consistency, and precision. Automated systems can assemble components, inspect products, and transport materials throughout production facilities. These capabilities improve operational efficiency while reducing worker exposure to potentially hazardous activities. However, introducing robotic systems requires careful consideration of maintenance requirements, employee training, and integration with existing production processes. Collaborative robots offer additional opportunities by operating alongside human workers in shared environments. As robotics technology continues to advance, manufacturers must balance productivity improvements with workplace safety and workforce development.""",

    """Biodiversity is fundamental to the stability and resilience of natural ecosystems. Different species contribute to ecological processes such as pollination, nutrient cycling, and population regulation. When habitats are destroyed or fragmented, these relationships can become disrupted, threatening the survival of vulnerable organisms. Conservation initiatives seek to protect biodiversity through habitat restoration, environmental regulations, and sustainable resource management. Community participation is particularly valuable because local populations often possess important knowledge about surrounding ecosystems. Long-term conservation success depends on cooperation among researchers, policymakers, and communities to address environmental challenges effectively.""",

    """Data science involves extracting meaningful insights from structured and unstructured information through statistical analysis, programming, and visualization. Before developing predictive models, analysts must evaluate the quality of their datasets and address problems such as missing values, inconsistent formatting, and duplicate records. Data preprocessing is essential because unreliable inputs can produce misleading conclusions regardless of the sophistication of the analytical method. Once datasets are prepared, visualization techniques help communicate patterns and relationships to stakeholders. Responsible data analysis also requires transparency about methodological limitations, potential biases, and the uncertainty associated with findings.""",

    """Biomedical engineering combines principles from engineering, biology, and medicine to develop technologies that address healthcare challenges. Researchers in this field design medical imaging systems, prosthetic devices, diagnostic instruments, and assistive technologies. Successful biomedical innovations require collaboration among engineers, healthcare professionals, and patients to ensure that solutions meet practical clinical needs. For example, wearable monitoring devices can collect physiological measurements and support ongoing observation outside traditional healthcare settings. However, these systems must satisfy demanding requirements involving accuracy, reliability, safety, and patient privacy before they can be integrated into routine medical practice.""",

    """The rapid development of emerging technologies has created important questions about accountability, transparency, and social responsibility. Automated decision-making systems increasingly influence activities ranging from employment screening to financial services. Although these tools can improve efficiency and consistency, poorly designed systems may reproduce biases present in their training data. Organizations developing such technologies should evaluate potential harms throughout the design and deployment process. Independent testing, accessible explanations, and meaningful human oversight can help reduce unintended consequences. Ethical technology development ultimately requires recognizing that technical performance alone does not determine whether a system benefits society.""",
]

# A separate set of examples for label coverage.
# These are candidate inputs, not guaranteed classifications.
# FP08 is a short genuine-human sample from the attack set.
# It is included to test label reachability, not detector accuracy.

LABEL_COVERAGE_TEXTS = [
    HUMAN_TEXTS[0],
    HUMAN_TEXTS[4],
    AI_TEXTS[0],
    AI_TEXTS[2],
    AI_TEXTS[7],
    HUMAN_TEXTS[8],
    "Went for a run. Legs hurt. Worth it.",
]

# Ten invalid request bodies for Criterion 5.

INVALID_BODIES = [
    {"text": "", "creator_id": "eval_invalid_01"},
    {"text": "   ", "creator_id": "eval_invalid_02"},
    {"creator_id": "eval_invalid_03"},
    {"text": "Missing creator ID."},
    {"text": None, "creator_id": "eval_invalid_05"},
    {"text": 12345, "creator_id": "eval_invalid_06"},
    {"text": ["not", "a", "string"], "creator_id": "eval_invalid_07"},
    {"text": "Invalid creator.", "creator_id": {"id": "invalid"}},
    {"text": "word " * 50000, "creator_id": "eval_invalid_09"},
    {"text": "Valid text.", "creator_id": ""},
]

SCENARIOS = [
    {
        "name": "human false positives",
        "criterion": 1,
        "texts": HUMAN_TEXTS,
    },
    {
        "name": "human score comparison",
        "criterion": 2,
        "texts": HUMAN_TEXTS,
    },
    {
        "name": "ai score comparison",
        "criterion": 2,
        "texts": AI_TEXTS,
    },
    {
        "name": "label coverage",
        "criterion": 3,
        "texts": LABEL_COVERAGE_TEXTS,
    },
    {
        "name": "invalid inputs",
        "criterion": 5,
        "bodies": INVALID_BODIES,
    },
]


def validate() -> list[str]:
    """
    Complain about anything malformed, before a long run rather than during.

    A "bodies" scenario is deliberately exempt from the empty check — an empty
    string is the whole point of a bad-input case, and refusing to run one
    would make that criterion untestable.
    """
    problems = []
    for i, scenario in enumerate(SCENARIOS, 1):
        if not scenario.get("name"):
            problems.append(f"scenario {i} has no name")

        texts = scenario.get("texts")
        bodies = scenario.get("bodies")

        if texts and bodies:
            problems.append(
                f"scenario {i} ('{scenario.get('name')}') has both texts and "
                f"bodies — pick one"
            )
            continue

        if bodies:
            for j, body in enumerate(bodies, 1):
                if not isinstance(body, dict):
                    problems.append(
                        f"scenario {i}, body {j} is not a dict — bodies are whole "
                        f"request bodies, like {{'text': '', 'creator_id': 'x'}}"
                    )
            continue

        if not texts:
            problems.append(f"scenario {i} has no texts and no bodies")
            continue

        for j, text in enumerate(texts, 1):
            if not str(text).strip():
                problems.append(
                    f"scenario {i}, text {j} is empty — if an empty submission is what "
                    f"you're testing, use 'bodies' instead of 'texts'"
                )
            elif str(text).startswith("REPLACE ME"):
                problems.append(
                    f"scenario {i} ('{scenario.get('name')}'), text {j} is still "
                    f"the placeholder"
                )

    return problems
