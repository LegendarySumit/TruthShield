"""
Universal Fact-Check Dataset Generator v3
==========================================
Generates a large, diverse dataset covering ALL types of claims people might
want to verify: health, science, history, tech, social media, urban legends,
finance, politics, everyday facts, and more.

The model learns to distinguish CREDIBLE vs NON-CREDIBLE text based on
linguistic patterns, writing style, sourcing, and rhetoric — NOT on the
actual truth/falsity of specific facts (that's what Gemini is for).

Target: 20,000+ samples with high combinatorial diversity.
"""

import pandas as pd
import random
import os
import re
import itertools

random.seed(42)

# ========================================================================
#  CREDIBLE / REAL TEMPLATES — factual, sourced, measured, professional
# ========================================================================

REAL_TEMPLATES = [
    # ---- ECONOMY / FINANCE ----
    "The Federal Reserve announced a {rate}% interest rate {direction} on {day}, citing {economic_reason}. Economists {reaction} the decision.",
    "According to the Bureau of Labor Statistics, the unemployment rate {moved} to {pct}% in {month}, {beating_missing} analysts' expectations of {pct2}%.",
    "The stock market {rose_fell} {points} points on {day} as investors reacted to {market_catalyst}. The S&P 500 closed at {sp_val}.",
    "GDP growth for {quarter} came in at {gdp_pct}%, {above_below} the {gdp_pct2}% forecast, according to the Commerce Department.",
    "{company} reported quarterly earnings of ${earnings} per share, {beating_missing} Wall Street estimates. Revenue reached ${revenue} billion.",
    "New IMF data shows global economic growth projected at {gdp_pct}% for {year}, {direction2} from {gdp_pct2}% the previous year.",
    "Consumer spending {rose_fell} by {pct}% in {month}, according to the Department of Commerce, driven by {spending_driver}.",
    "The World Bank projects that developing nations will see {gdp_pct}% growth in {year}, supported by {development_factor}.",

    # ---- POLITICS (neutral, factual) ----
    "President {president} signed {bill_name} into law on {day}, a measure that {bill_desc}. The legislation passed with bipartisan support.",
    "The {chamber} voted {vote_for}-{vote_against} to approve {bill_name}, which would {bill_desc}.",
    "Secretary of State {official} met with {foreign_leader} in {city} to discuss {diplomatic_topic}. Both sides described the talks as productive.",
    "The Supreme Court agreed to hear arguments in {case_name}, a case concerning {legal_topic}. Oral arguments are scheduled for {month}.",
    "Voter turnout in the {us_state} {election_type} reached {turnout_pct}%, according to the state's election commission.",
    "A bipartisan committee released its report on {policy_topic}, recommending {num_recs} changes to existing regulations.",
    "The Congressional Budget Office estimated the proposed legislation would {budget_impact} over the next decade.",

    # ---- SCIENCE / RESEARCH ----
    "Researchers at {university} published a study in {journal} showing that {science_finding}. The study involved {num_participants} participants over {study_period}.",
    "NASA announced the successful launch of {mission_name} from {launch_site} on {day}. The spacecraft is expected to reach {destination} in approximately {travel_time}.",
    "A team of scientists from {institution} discovered {discovery}, according to findings published in {journal}.",
    "Climate data from {source_org} indicates that global average temperature in {year} was {temp_change} degrees above the pre-industrial baseline.",
    "A new peer-reviewed study in {journal} found that {health_finding}. Researchers emphasized the need for further investigation.",
    "The {institution} research team confirmed that {science_confirmation}, based on data collected from {data_source} over {study_period}.",
    "According to a meta-analysis of {meta_num} studies published in {journal}, {meta_finding}.",
    "Scientists at {institution} developed a new {tech_innovation} that could {tech_benefit}, though they note further testing is required.",

    # ---- HEALTH / MEDICINE (evidence-based) ----
    "The World Health Organization reported that global cases of {disease} {rose_fell2} by {pct}% compared to the previous {time_period}, attributing the change to {health_reason}.",
    "A clinical trial conducted by {university} found that {drug_name} {drug_effect} in patients with {condition}. The results were published in {journal}.",
    "The CDC recommends that adults get at least {exercise_mins} minutes of moderate-intensity exercise per week to reduce the risk of {health_condition}.",
    "According to the American Heart Association, approximately {health_stat_num} million Americans are affected by {health_condition} each year.",
    "Research published in {journal} suggests that {diet_finding}, though researchers note the study was observational and more research is needed.",
    "The FDA approved {drug_name} for the treatment of {condition} after a Phase III trial showed {trial_result}.",
    "Public health officials in {us_state} reported that vaccination rates for {vaccine_type} reached {vax_rate}% among eligible residents.",
    "A systematic review published in {journal} examined {meta_num} studies and found that {health_finding}.",
    "The National Institutes of Health announced ${research_funding} million in funding for research into {research_topic}.",

    # ---- TECHNOLOGY (factual, balanced) ----
    "According to a report by {tech_firm}, {tech_stat} in {year}. The data suggests {tech_implication}.",
    "{company} announced the launch of {product_name}, which features {product_feature}. The product will be available starting {month}.",
    "A study by {university} researchers found that {tech_finding}. The research was presented at {tech_conference}.",
    "The {tech_agency} released new guidelines for {tech_regulation_topic}, requiring companies to {tech_requirement}.",
    "Global smartphone shipments {rose_fell} by {pct}% in {quarter}, according to data from {tech_firm}.",
    "Cybersecurity researchers at {institution} identified {cyber_finding}. They recommend {cyber_recommendation}.",
    "AI systems developed by {company} achieved {ai_benchmark} on {ai_task}, according to results published in {journal}.",

    # ---- HISTORY (factual statements) ----
    "The {historical_event} occurred in {hist_year}, resulting in {historical_consequence}. Historians widely agree on these facts based on extensive documentation.",
    "According to historical records, {historical_figure} {historical_action} in {hist_year}, which led to {historical_consequence}.",
    "Archaeological evidence from {archaeological_site} confirms that {archaeological_finding}, dating back approximately {hist_age} years.",
    "The {historical_document} was {hist_doc_action} in {hist_year}, establishing {hist_doc_impact}.",
    "Historical census data shows that the population of {country} was approximately {population} million in {hist_year}.",

    # ---- ENVIRONMENT / CLIMATE ----
    "According to {source_org}, global CO2 concentrations reached {co2_level} parts per million in {year}, continuing an upward trend.",
    "A report by the {env_org} found that {env_finding}. The study analyzed data from {env_data_source} spanning {study_period}.",
    "Renewable energy sources accounted for {renewable_pct}% of electricity generation in {country} in {year}, according to {source_org}.",
    "The {env_org} reported that deforestation rates in {region} {rose_fell2} by {pct}% compared to the previous year.",
    "Ocean temperatures in the {ocean} reached record levels in {year}, according to measurements by {source_org}, raising concerns about coral reef health.",

    # ---- EDUCATION / EVERYDAY ----
    "City officials in {city} approved a ${amount} million plan to {city_project}. Construction is expected to begin in {month}.",
    "The local school district announced plans to {education_plan}, affecting approximately {num_students} students across {num_schools} schools.",
    "Transit authorities approved expanded service on the {transit_line} line, adding {num_trains} additional trains during peak hours.",
    "A wildfire in {us_state} has burned approximately {acres} acres as of {day}, with firefighters reporting {containment_pct}% containment.",
    "The {sports_team} defeated the {opponent} {score} in {event}, securing their place in the {round}.",
    "The U.S. Census Bureau reported that {us_state}'s population grew by {pct}% over the last decade, driven largely by {pop_driver}.",

    # ---- GENERAL KNOWLEDGE (factual, encyclopedic) ----
    "Water boils at 100 degrees Celsius (212 degrees Fahrenheit) at standard atmospheric pressure, a physical constant established through thermodynamic research.",
    "The speed of light in a vacuum is approximately 299,792 kilometers per second, as confirmed by numerous experiments since the 17th century.",
    "The human body contains approximately 206 bones in adults, according to standard anatomy references used in medical education.",
    "Photosynthesis is the process by which plants convert carbon dioxide and water into glucose and oxygen, using energy from sunlight.",
    "The Earth orbits the Sun once approximately every 365.25 days, which is why a leap year is added every four years to keep the calendar aligned.",
    "DNA (deoxyribonucleic acid) carries the genetic instructions for the development and functioning of all known living organisms.",
    "The Pacific Ocean is the largest and deepest ocean on Earth, covering more than 63 million square miles.",
    "Antibiotics work by targeting bacterial cells and are ineffective against viral infections, which is why doctors recommend against using them for the common cold.",
    "According to NASA, the average distance from the Earth to the Moon is approximately 384,400 kilometers.",
    "The periodic table of elements currently contains 118 confirmed elements, organized by atomic number and chemical properties.",
    "Gravity is a fundamental force of nature that attracts objects with mass toward each other, described by Newton's law of universal gravitation and later refined by Einstein's general relativity.",
    "The Great Wall of China is approximately {wall_length} kilometers long including all branches and sections, according to a comprehensive survey by China's State Administration of Cultural Heritage.",
    "Mount Everest stands at approximately 8,849 meters above sea level, as measured by the most recent survey conducted jointly by China and Nepal in 2020.",
    "The Amazon Rainforest covers approximately 5.5 million square kilometers across nine countries in South America, according to the World Wildlife Fund.",

    # ---- EXPERT COMMENTARY / BALANCED ANALYSIS ----
    "Experts at {university} noted that {balanced_claim}. While {caveat_positive}, they also cautioned that {caveat_negative}.",
    "According to {expert_title} {expert_name} from {institution}, {expert_opinion}. However, other researchers in the field suggest {alternate_view}.",
    "A panel of experts convened by {source_org} concluded that {expert_conclusion}, while emphasizing that {expert_caveat}.",

    # ---- SHORT CREDIBLE CLAIMS ----
    "{verified_short_fact}",
    "{verified_short_fact}",
    "{verified_short_fact}",
    "{verified_short_fact}",
]

REAL_FILLERS = {
    # Economy
    "rate": ["0.25", "0.50", "0.75", "0.10", "1.00"],
    "direction": ["increase", "decrease", "hold"],
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "economic_reason": ["persistent inflation concerns", "slowing economic growth", "strong labor market data", "easing supply chain pressures", "rising consumer confidence"],
    "reaction": ["largely supported", "debated the merits of", "expressed mixed views on", "cautiously welcomed"],
    "sector": ["housing", "consumer spending", "small businesses", "international trade", "manufacturing"],
    "moved": ["dropped", "rose", "remained steady", "fell slightly", "edged up"],
    "pct": ["3.4", "3.7", "4.1", "3.9", "5.2", "4.8", "2.1", "6.3", "1.8"],
    "pct2": ["3.5", "3.8", "4.0", "4.2", "5.0", "4.6", "2.3", "6.0", "2.0"],
    "month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "beating_missing": ["beating", "missing", "matching", "slightly exceeding", "narrowly missing"],
    "rose_fell": ["rose", "fell", "gained", "lost", "climbed", "declined"],
    "points": ["150", "212", "85", "310", "47", "523", "198", "67", "402"],
    "market_catalyst": ["better-than-expected earnings reports", "new trade deal announcements", "inflation data", "oil price fluctuations", "tech sector performance", "Federal Reserve commentary", "strong jobs data"],
    "sp_val": ["4,523", "5,012", "4,890", "5,134", "4,678", "5,280", "5,450"],
    "quarter": ["Q1 2025", "Q2 2025", "Q3 2024", "Q4 2024", "Q1 2026", "Q2 2026"],
    "gdp_pct": ["2.1", "1.8", "3.2", "2.5", "2.9", "1.4", "3.5", "0.8"],
    "gdp_pct2": ["2.0", "1.9", "3.0", "2.3", "2.7", "1.6", "3.3", "1.0"],
    "above_below": ["above", "below", "in line with"],
    "company": ["Apple", "Microsoft", "Amazon", "Google", "Tesla", "Meta", "Johnson & Johnson", "Pfizer", "Toyota", "Samsung", "Intel", "Netflix", "Uber", "Nvidia"],
    "earnings": ["1.52", "2.13", "0.98", "3.45", "1.87", "2.76", "4.12", "0.67"],
    "revenue": ["24.5", "18.3", "32.1", "7.8", "12.4", "45.6", "8.9", "61.2"],
    "year": ["2024", "2025", "2026"],
    "direction2": ["up", "down", "unchanged"],
    "spending_driver": ["holiday season purchases", "increased housing activity", "back-to-school spending", "rising wages"],
    "development_factor": ["increased foreign investment", "infrastructure spending", "technology adoption", "agricultural productivity gains"],

    # Politics
    "president": ["the President", "Biden", "the administration", "the White House"],
    "bill_name": ["the Infrastructure Investment Act", "the Education Modernization Act", "the Clean Energy Transition Act", "a new defense spending authorization", "the Healthcare Access Act", "the Digital Privacy Protection Act", "the Water Resources Act"],
    "bill_desc": ["allocates funding for bridge and road repairs", "expands access to early education programs", "provides tax incentives for renewable energy", "modernizes cybersecurity protocols", "extends insurance coverage options", "establishes new data privacy standards"],
    "chamber": ["the Senate", "the House of Representatives", "Congress"],
    "next_chamber": ["the Senate", "the House"],
    "vote_for": ["67", "54", "72", "231", "218", "289", "63"],
    "vote_against": ["33", "46", "28", "198", "212", "143", "37"],
    "official": ["Blinken", "the Secretary", "Sullivan", "the diplomat"],
    "foreign_leader": ["foreign dignitaries", "regional leaders", "EU officials", "NATO allies", "G7 representatives"],
    "city": ["Washington", "Geneva", "Tokyo", "London", "Brussels", "Seoul", "Beijing", "Austin", "Denver", "Portland", "Berlin", "Paris", "Ottawa", "Canberra", "New Delhi"],
    "diplomatic_topic": ["trade agreements", "climate policy coordination", "defense cooperation", "humanitarian aid", "cybersecurity", "nuclear nonproliferation"],
    "case_name": ["Smith v. United States", "Gonzalez v. State Board", "National Association v. Department", "Parker v. Federal Agency"],
    "legal_topic": ["digital privacy rights", "environmental regulations", "interstate commerce", "voting district boundaries", "First Amendment protections"],
    "us_state": ["California", "Texas", "Florida", "Ohio", "Michigan", "Pennsylvania", "Georgia", "Arizona", "Colorado", "Oregon", "New York", "Illinois", "Virginia", "Washington", "Minnesota"],
    "election_type": ["primary", "general election", "special election", "midterm"],
    "turnout_pct": ["62", "58", "71", "45", "67", "73", "55"],
    "turnout_pct2": ["59", "55", "68", "42", "64", "70", "52"],
    "policy_topic": ["immigration reform", "healthcare funding", "education standards", "transportation infrastructure", "broadband access"],
    "num_recs": ["12", "8", "15", "6", "20", "9"],
    "budget_impact": ["reduce the deficit by $120 billion", "increase spending by $85 billion", "be revenue-neutral", "cost approximately $200 billion"],

    # Science
    "university": ["MIT", "Stanford", "Johns Hopkins", "the University of Oxford", "Harvard", "Caltech", "UC Berkeley", "Cambridge", "ETH Zurich", "the University of Tokyo", "Columbia University", "Yale", "Princeton", "the Max Planck Institute"],
    "journal": ["Nature", "Science", "The Lancet", "JAMA", "Cell", "PNAS", "The New England Journal of Medicine", "Nature Medicine", "Physical Review Letters", "IEEE Transactions"],
    "science_finding": [
        "a new compound may slow the progression of Alzheimer's disease",
        "exercise significantly reduces the risk of cardiovascular events in older adults",
        "microplastics are present in a wider range of food products than previously thought",
        "a gene therapy approach shows promise in treating sickle cell disease",
        "ocean acidification is accelerating in polar regions",
        "a specific protein plays a key role in immune response regulation",
        "sleep patterns significantly influence memory consolidation",
        "urban green spaces are associated with lower rates of depression",
    ],
    "num_participants": ["1,200", "5,000", "850", "15,000", "3,400", "800", "50,000", "2,100"],
    "study_period": ["3 years", "18 months", "5 years", "10 months", "2 years", "8 years", "6 months"],
    "mission_name": ["the Artemis III mission", "the Mars Sample Return probe", "a new Earth observation satellite", "the Europa Clipper spacecraft", "the OSIRIS-REx mission"],
    "launch_site": ["Kennedy Space Center", "Vandenberg Space Force Base", "Cape Canaveral", "Baikonur Cosmodrome"],
    "destination": ["the Moon", "Mars orbit", "Jupiter's moon Europa", "low Earth orbit", "the asteroid belt"],
    "travel_time": ["6 months", "3 days", "2 years", "6 weeks", "9 months"],
    "institution": ["the Max Planck Institute", "CERN", "the National Institutes of Health", "the Salk Institute", "MIT Lincoln Laboratory", "the Jet Propulsion Laboratory", "the Pasteur Institute", "the Broad Institute"],
    "discovery": ["a new species of deep-sea organism", "a potential biomarker for early cancer detection", "evidence of ancient water on Mars", "a novel approach to quantum error correction", "a new class of antibiotics derived from soil bacteria"],
    "field": ["oncology", "marine biology", "planetary science", "quantum computing", "materials science", "neuroscience", "immunology"],
    "science_confirmation": [
        "certain genetic markers are associated with increased risk of heart disease",
        "the universe is expanding at an accelerating rate",
        "microplastics have been detected in human blood samples",
        "a particular enzyme pathway contributes to drug resistance in bacteria",
    ],
    "data_source": ["satellite imagery", "clinical records across 12 hospitals", "geological surveys", "genomic sequencing databases", "ocean buoy measurements"],
    "meta_num": ["47", "128", "83", "215", "64", "32"],
    "meta_finding": [
        "regular physical activity is associated with a 20-30% reduction in all-cause mortality",
        "early childhood education programs show lasting positive effects on academic achievement",
        "mindfulness-based interventions can reduce symptoms of anxiety and depression",
        "moderate coffee consumption is not associated with increased cardiovascular risk",
    ],
    "tech_innovation": ["battery technology", "semiconductor material", "AI architecture", "water purification method", "carbon capture technique"],
    "tech_benefit": ["extend electric vehicle range by 40%", "reduce computing energy costs", "improve early disease detection accuracy", "provide clean water in remote areas", "remove CO2 from industrial emissions"],

    # Health
    "disease": ["malaria", "tuberculosis", "measles", "dengue fever", "influenza", "diabetes", "HIV"],
    "rose_fell2": ["decreased", "increased", "remained stable", "declined", "grew"],
    "time_period": ["year", "quarter", "month", "decade"],
    "health_reason": ["expanded vaccination programs", "seasonal factors", "improved diagnostic capabilities", "public health interventions", "increased awareness"],
    "drug_name": ["a new monoclonal antibody treatment", "an mRNA-based therapy", "a modified version of an existing drug", "a novel immunotherapy agent"],
    "drug_effect": ["showed significant improvement in symptoms", "reduced disease progression by 35%", "improved survival rates", "reduced inflammatory markers"],
    "condition": ["rheumatoid arthritis", "type 2 diabetes", "chronic heart failure", "treatment-resistant depression", "advanced melanoma", "chronic kidney disease"],
    "exercise_mins": ["150", "75", "300"],
    "health_condition": ["cardiovascular disease", "type 2 diabetes", "stroke", "obesity", "hypertension", "certain types of cancer"],
    "health_stat_num": ["6", "34", "18", "3.5", "12"],
    "diet_finding": [
        "a Mediterranean diet is associated with reduced cardiovascular risk",
        "adequate fiber intake may lower the risk of colorectal cancer",
        "excessive processed meat consumption is linked to higher cancer risk",
        "omega-3 fatty acids may support cognitive function in older adults",
    ],
    "trial_result": ["a statistically significant improvement in primary endpoints", "a 42% reduction in disease progression", "favorable safety and efficacy data"],
    "vaccine_type": ["influenza", "COVID-19", "HPV", "measles", "chickenpox"],
    "vax_rate": ["72", "85", "91", "68", "78"],
    "health_finding": [
        "moderate coffee consumption is associated with a lower risk of type 2 diabetes",
        "regular sleep schedules improve cognitive performance in children",
        "air pollution exposure may increase the risk of respiratory infections",
        "adequate hydration is important for kidney function",
        "regular physical activity may reduce the risk of developing depression",
    ],
    "research_funding": ["50", "120", "250", "75", "300"],
    "research_topic": ["Alzheimer's disease", "cancer immunotherapy", "antibiotic resistance", "mental health", "rare genetic disorders"],

    # Technology
    "tech_firm": ["Gartner", "IDC", "Statista", "McKinsey", "Deloitte", "Pew Research"],
    "tech_stat": [
        "global AI spending exceeded $150 billion",
        "over 4.5 billion people now use social media",
        "cybercrime damages are projected to reach $10 trillion annually",
        "cloud computing adoption reached 94% among enterprises",
    ],
    "tech_implication": [
        "continued rapid growth in the sector",
        "a shift in how businesses approach digital transformation",
        "growing need for improved cybersecurity infrastructure",
        "increasing importance of data privacy regulations",
    ],
    "product_name": ["its next-generation processor", "an updated AI assistant", "a new cloud platform", "an electric vehicle model", "a mixed-reality headset"],
    "product_feature": ["improved energy efficiency", "advanced machine learning capabilities", "enhanced security features", "faster processing speeds", "extended battery life"],
    "tech_finding": [
        "social media use of more than 4 hours daily is associated with increased anxiety in teens",
        "AI-generated text can be detected with approximately 80% accuracy using current tools",
        "remote work increases productivity by 13% on average according to a controlled study",
        "two-factor authentication reduces account compromise by over 99%",
    ],
    "tech_conference": ["NeurIPS", "CES 2026", "the IEEE Symposium", "Google I/O", "WWDC", "re:Invent"],
    "tech_agency": ["Federal Trade Commission", "European Commission", "FCC", "Department of Commerce"],
    "tech_regulation_topic": ["AI transparency", "data privacy", "algorithmic bias", "children's online safety"],
    "tech_requirement": ["disclose AI usage in content generation", "provide data deletion options to users", "conduct regular algorithmic audits", "implement age verification systems"],
    "cyber_finding": ["a new vulnerability in widely used authentication protocols", "a sophisticated phishing campaign targeting healthcare workers", "a zero-day exploit affecting major operating systems"],
    "cyber_recommendation": ["updating software immediately", "enabling multi-factor authentication", "reviewing access permissions"],
    "ai_benchmark": ["state-of-the-art performance", "94.5% accuracy", "a 15% improvement over previous methods"],
    "ai_task": ["natural language understanding", "medical image analysis", "protein structure prediction", "code generation"],

    # History
    "historical_event": ["signing of the Treaty of Versailles", "fall of the Berlin Wall", "Apollo 11 Moon landing", "end of World War II", "signing of the Declaration of Independence", "Cuban Missile Crisis"],
    "hist_year": ["1776", "1865", "1914", "1945", "1969", "1989", "1991", "2001", "1492", "1215"],
    "historical_consequence": ["significant geopolitical changes", "the establishment of new international institutions", "a shift in global power dynamics", "lasting impacts on civil rights", "major territorial changes"],
    "historical_figure": ["Abraham Lincoln", "Marie Curie", "Mahatma Gandhi", "Winston Churchill", "Rosa Parks", "Nelson Mandela", "Albert Einstein"],
    "historical_action": ["delivered a landmark address", "made a groundbreaking discovery", "led a major social movement", "signed a historic agreement", "established key institutions"],
    "archaeological_site": ["Göbekli Tepe in Turkey", "Pompeii in Italy", "the Egyptian Valley of the Kings", "Machu Picchu in Peru", "the caves of Lascaux in France"],
    "archaeological_finding": ["advanced engineering was used in ancient construction", "trade networks extended farther than previously believed", "early humans had more sophisticated tools than expected"],
    "hist_age": ["2,000", "5,000", "10,000", "3,500", "40,000"],
    "historical_document": ["Magna Carta", "U.S. Constitution", "Universal Declaration of Human Rights", "Treaty of Westphalia", "Emancipation Proclamation"],
    "hist_doc_action": ["signed", "ratified", "adopted", "proclaimed"],
    "hist_doc_impact": ["fundamental principles of governance", "foundational human rights protections", "new international legal standards", "landmark civil rights protections"],
    "country": ["the United States", "China", "India", "Germany", "Japan", "Brazil", "the United Kingdom", "France"],
    "population": ["331", "1,400", "1,380", "83", "125", "212", "67", "65"],

    # Environment
    "source_org": ["NOAA", "the European Space Agency", "the World Meteorological Organization", "the IPCC", "NASA", "the EPA", "the UN Environment Programme"],
    "co2_level": ["421", "425", "418", "430"],
    "env_org": ["the UN Environment Programme", "the World Wildlife Fund", "the Environmental Protection Agency", "the Intergovernmental Panel on Climate Change"],
    "env_finding": [
        "global biodiversity has declined by 69% since 1970",
        "single-use plastic production has doubled in the last two decades",
        "Arctic sea ice extent reached a new seasonal low",
        "methane emissions from agriculture are higher than previously estimated",
    ],
    "env_data_source": ["satellite observations", "ground-based monitoring stations", "ocean buoy networks", "ice core samples"],
    "renewable_pct": ["22", "35", "45", "18", "52", "80"],
    "region": ["the Amazon Basin", "Southeast Asia", "Sub-Saharan Africa", "Central America", "the Congo Basin"],
    "ocean": ["Pacific", "Atlantic", "Indian", "Arctic"],
    "temp_change": ["1.2", "1.1", "1.3", "1.48", "1.5"],

    # Everyday / Education
    "amount": ["45", "120", "200", "78", "15", "250", "30"],
    "city_project": ["renovate the downtown transit hub", "build a new community recreation center", "expand the water treatment facility", "upgrade public school buildings", "construct a new public library"],
    "education_plan": ["introduce a revised STEM curriculum", "hire 200 additional teachers", "expand after-school tutoring programs", "implement a new literacy initiative"],
    "num_students": ["12,000", "8,500", "25,000", "5,000", "18,000"],
    "num_schools": ["18", "24", "35", "12", "42"],
    "transit_line": ["Blue", "Red", "Green", "Orange", "Silver"],
    "num_trains": ["6", "10", "8", "12", "4"],
    "acres": ["3,500", "12,000", "800", "25,000", "5,200"],
    "containment_pct": ["35", "60", "85", "15", "50", "92"],
    "sports_team": ["Lakers", "Barcelona", "Yankees", "Patriots", "Warriors", "Real Madrid", "Manchester City"],
    "opponent": ["Celtics", "Real Madrid", "Red Sox", "Bills", "Nuggets", "Liverpool", "Bayern Munich"],
    "score": ["3-1", "102-98", "4-2", "24-17", "2-0", "110-105"],
    "event": ["last night's game", "Sunday's match", "the championship series", "the semifinal"],
    "round": ["semifinals", "finals", "next round of playoffs", "quarterfinals"],
    "pop_driver": ["immigration", "economic growth", "birth rate increases", "domestic migration"],

    # General Knowledge
    "wall_length": ["21,196", "6,259"],

    # Expert commentary
    "balanced_claim": [
        "AI has the potential to significantly improve healthcare diagnostics",
        "renewable energy technology has advanced rapidly in the last decade",
        "remote work offers benefits for both employers and employees",
        "social media platforms face complex content moderation challenges",
    ],
    "caveat_positive": [
        "the technology shows remarkable promise",
        "early results are encouraging",
        "the economic benefits are clear",
        "there are significant potential advantages",
    ],
    "caveat_negative": [
        "significant regulatory and ethical challenges remain",
        "long-term effects are still not fully understood",
        "equitable access continues to be a challenge",
        "privacy concerns must be carefully addressed",
    ],
    "expert_title": ["Professor", "Dr.", "Research Director"],
    "expert_name": ["Sarah Chen", "Michael Rodriguez", "Emily Watson", "David Kim", "Amara Johnson"],
    "expert_opinion": [
        "the evidence supports a cautious but optimistic approach",
        "current data indicates meaningful progress in the field",
        "the findings are consistent with previous research",
        "this represents a significant advancement, though not a breakthrough",
    ],
    "alternate_view": [
        "more data is needed before drawing definitive conclusions",
        "the methodology could be improved in future studies",
        "real-world applications may differ from laboratory results",
        "the effect size may be smaller than initially reported",
    ],
    "expert_conclusion": [
        "the evidence strongly supports the effectiveness of early intervention",
        "climate adaptation strategies are essential alongside mitigation efforts",
        "investment in STEM education yields measurable economic returns",
    ],
    "expert_caveat": [
        "implementation details will determine real-world outcomes",
        "resource constraints may limit near-term adoption",
        "cultural and regional differences should be considered",
    ],

    # Short verified facts
    "verified_short_fact": [
        "The Earth revolves around the Sun, completing one orbit approximately every 365.25 days. This heliocentric model has been confirmed by centuries of astronomical observation.",
        "Water is composed of two hydrogen atoms and one oxygen atom (H2O). This chemical composition was established through electrolysis experiments in the early 19th century.",
        "The speed of sound in air at sea level is approximately 343 meters per second. This varies with temperature, humidity, and altitude.",
        "Vaccines work by training the immune system to recognize and fight pathogens. The CDC and WHO recommend vaccination based on extensive clinical trial data.",
        "The human heart beats approximately 100,000 times per day. This rate varies based on age, fitness level, and activity.",
        "Light from the Sun takes approximately 8 minutes and 20 seconds to reach Earth. This is because the Sun is about 150 million kilometers away.",
        "The Sahara Desert is the largest hot desert in the world, covering approximately 9.2 million square kilometers across North Africa.",
        "Penicillin, the first widely used antibiotic, was discovered by Alexander Fleming in 1928. This discovery revolutionized the treatment of bacterial infections.",
        "The human genome contains approximately 3 billion base pairs of DNA. The Human Genome Project completed its mapping in 2003.",
        "The boiling point of water decreases at higher altitudes due to lower atmospheric pressure. This is why cooking takes longer at high elevations.",
        "The International Space Station orbits the Earth approximately every 90 minutes at an altitude of about 400 kilometers.",
        "Carbon dioxide is a greenhouse gas that traps heat in the atmosphere. Its concentration has increased from about 280 ppm pre-industrial to over 420 ppm today.",
        "Earthquakes are caused by the movement of tectonic plates beneath the Earth's surface. The Richter scale measures the magnitude of seismic events.",
        "The Amazon River is the largest river by discharge volume in the world, carrying more water than the next seven largest rivers combined.",
        "Insulin is a hormone produced by the pancreas that regulates blood sugar levels. Its discovery in 1921 transformed the treatment of diabetes.",
        "The average depth of the world's oceans is approximately 3,688 meters (12,100 feet), according to NOAA measurements.",
        "According to geological evidence, the Earth is approximately 4.54 billion years old. This age is determined through radiometric dating of rocks.",
        "Plate tectonics is the scientific theory that Earth's outer shell is divided into large plates that move, float, and sometimes fracture. This theory explains earthquakes, volcanoes, and mountain formation.",
        "The Milky Way galaxy contains an estimated 100 to 400 billion stars, according to astronomical surveys.",
        "Human-caused climate change is supported by the overwhelming consensus of climate scientists, as documented in multiple IPCC assessment reports.",
    ],
}


# ========================================================================
#  FAKE / NON-CREDIBLE TEMPLATES — sensational, misleading, manipulative
# ========================================================================

FAKE_TEMPLATES = [
    # ---- CONSPIRACY / ALARMIST ----
    "BREAKING: {fake_group} caught in massive cover-up — {fake_conspiracy}!! They don't want you to know this! Share before it's deleted!!!",
    "EXPOSED: {fake_authority} secretly {fake_action}. Whistleblower reveals SHOCKING truth about everything you thought you knew!",
    "Scientists STUNNED: {fake_science_claim}! Big Pharma has been HIDING this from the public for decades!",
    "URGENT: {fake_health_claim}! Doctors are BAFFLED. This simple {remedy} has been suppressed by the medical establishment!",
    "{fake_group} just BANNED {fake_banned_thing}! This is the beginning of the end of freedom as we know it!!!",
    "LEAKED document proves {fake_leak_claim}! The government has been lying to us for YEARS. Wake up people!!!",
    "WARNING: {fake_warning}. The mainstream media is covering this up. Spread this NOW before they take it down!",
    "PROOF that {fake_proof_claim}! Top insider finally breaks silence and reveals what's REALLY going on!",
    "TOP SECRET: {fake_authority} has been {fake_action} for {years} years and {person_type} just confirmed it!!",
    "WAKE UP: {fake_conspiracy}!! This is NOT a conspiracy theory anymore — {fake_group} has been caught red-handed!!!",
    "CONFIRMED: {fake_authority} insider admits {fake_leak_claim}! This BOMBSHELL will bring down the entire system!",

    # ---- CLICKBAIT / MISLEADING ----
    "This one weird trick {fake_trick_claim}. Doctors HATE it! Number 7 will shock you!",
    "MIRACLE cure discovered: {fake_cure_claim}. Why isn't the media reporting on this??",
    "Study PROVES that {fake_study_claim}. The results are MIND-BLOWING and will change everything!",
    "You WON'T BELIEVE what {fake_celebrity} just said about {fake_topic}! The internet is going CRAZY!",
    "{fake_celebrity} spotted with {fake_sighting}! Fans are in COMPLETE SHOCK. Is this proof of {fake_conclusion}??",
    "FINALLY: The real reason {fake_suppressed_reason}. This information has been suppressed for {years} years!",
    "Exclusive: Anonymous source inside {fake_institution} reveals {fake_insider_info}. This changes EVERYTHING!",
    "You have {hours} hours to do THIS or {fake_consequence}! The government won't tell you about this!",
    "What {fake_celebrity} did {time_ago} SHOOK the entire world! You need to see this before they take it down!",
    "{person_type} exposed the REAL truth about {fake_topic}! The video went viral and they're trying to delete it!",
    "TOP 10 things {fake_group} doesn't want you to know about {fake_topic}! Number {list_num} will leave you SPEECHLESS!!!",

    # ---- HEALTH MISINFORMATION ----
    "Exposed: {fake_vaccine_claim}! Your doctor WON'T tell you this. Brave researchers risked everything to expose this!",
    "This common {food_item} is actually {fake_food_claim}! Scientists confirm what we've been saying for years!",
    "HIDDEN DANGER: {hidden_danger_claim}! The FDA has been covering this up. Watch this before they ban it!",
    "SECRET ingredient in {everyday_item} linked to {fake_health_link}! You'll NEVER use it again after reading this!",
    "EXPOSED: Hospitals are being PAID to {fake_health_scam}! A brave {person_type} just leaked internal documents!",
    "The {food_item} you eat every day is DESTROYING your {body_part}! Exposed by a scientist who was FIRED for speaking out!",
    "WARNING: {everyday_item} contains {hidden_substance} that causes {fake_health_link}! Why hasn't the FDA warned us?!",
    "EXPOSED: {fake_health_claim}! Exposed by brave researchers who risked everything! What {fake_group} doesn't want you to know!",
    "THIS {food_item} cures {real_disease} in just {days} days according to studies HIDDEN by {fake_group}! No doctor will tell you this!",

    # ---- SCIENCE DENIAL ----
    "EXPOSED: {science_denial_claim}! The scientific establishment has been LYING to you for {years} years! Open your eyes!",
    "PROOF that {science_denial_proof}! Independent researchers finally broke through the wall of lies! Share before this is censored!",
    "A brave {person_type} just revealed that {science_denial_claim}! The mainstream scientific community REFUSED to publish the truth!",
    "THEY DON'T WANT YOU TO KNOW: {science_denial_proof}! This changes everything you were taught in school!!!",
    "After {years} years of research, independent {person_type} proves {science_denial_claim}! The evidence is UNDENIABLE now!",

    # ---- POLITICAL MISINFORMATION ----
    "{political_target} secretly {fake_political_action}! Documents PROVE what we suspected all along! MSM silent!",
    "EXPOSED: The {election_conspiracy} during the last election. Millions of {election_fraud_type} confirmed!",
    "NEW WORLD ORDER: {nwo_claim}. This is NOT a drill. The elite have been planning this for decades!",
    "{fake_country} just made a secret deal with {fake_country2} to {fake_deal}. The media is SILENT!",
    "Deep state operatives caught {deep_state_action}. This is the biggest scandal in history and NO ONE is talking about it!",
    "LEAKED emails prove {political_target} has been {deep_state_action} since {fake_year}! The evidence is OVERWHELMING!",

    # ---- FINANCIAL SCAMS ----
    "BREAKING: Kid from {scam_city} discovers way to make ${fake_amount} per day from home! Banks HATE this trick!",
    "Elon Musk just endorsed {fake_crypto}! Invest now before it goes to the MOON! Limited spots available!!",
    "ALERT: The dollar is about to COLLAPSE! {financial_panic_claim}. Buy {safe_asset} NOW before it's too late!",
    "{fake_celebrity} reveals secret investment that turns ${small_amount} into ${fake_amount} in just {days} days!",
    "A {age}-year-old from {scam_city} just made ${fake_amount} in {days} days using this ONE WEIRD trick! Banks are FURIOUS!",
    "SHOCKING: {person_type} accidentally reveals the {safe_asset} loophole that {fake_group} has been hiding!",

    # ---- URBAN LEGENDS / HOAXES ----
    "CONFIRMED: {urban_legend}! Multiple {person_type} have verified this! Why isn't the media covering it??",
    "REAL VIDEO: {urban_legend}! This footage is going VIRAL and {fake_group} is desperately trying to suppress it!!!",
    "JUST IN: {urban_legend}! Footage captured on {camera_type} proves this beyond any doubt! Still think it's a myth??",
    "WARNING to all parents: {parent_scare}! This is HAPPENING in {scam_city} right now! Share to protect your family!",
    "PROOF caught on camera: {urban_legend}! The government ADMITS it's real but says 'don't panic'! We should ALL be panicking!!!",

    # ---- SOCIAL MEDIA / WHATSAPP STYLE ----
    "FORWARD THIS TO EVERYONE!! {chain_message} This is NOT a joke! Government confirmed! Send to {forward_num} people NOW!",
    "URGENT MESSAGE from {fake_authority}: {chain_message} Please share with all your contacts immediately! Time is running out!",
    "ATTENTION: {whatsapp_scare}! My {relative} works at {fake_institution} and confirmed this is 100% TRUE! Please share!",
    "Do NOT {dont_do_thing} starting {day}!! {whatsapp_scare}! A {person_type} from {fake_institution} just told me personally!",
    "VERIFIED by {fake_authority}: {chain_message} If you don't share this in {hours} hours, {fake_consequence}!",

    # ---- FAKE HISTORY / REVISIONISM ----
    "HIDDEN TRUTH: {fake_history_claim}! Your history books were REWRITTEN to hide this! The evidence is irrefutable!",
    "What they DON'T teach you in school: {fake_history_claim}! The real history has been covered up for centuries!",
    "Ancient texts PROVE {fake_ancient_claim}! Mainstream historians are TERRIFIED of this discovery!",
    "BOMBSHELL: Newly discovered documents prove {fake_history_claim}! Everything you learned in school was a LIE!",

    # ---- FAKE TECH / AI SCARES ----
    "EXPOSED: {fake_tech_claim}! Tech insiders have been warning about this for years but nobody listened!",
    "{company_fake} just admitted that {fake_tech_admission}! Delete your {tech_product} NOW before it's too late!",
    "Scientists TERRIFIED: {fake_ai_claim}! This is NOT science fiction — it's happening RIGHT NOW and no one is stopping it!",
    "LEAKED internal memo from {company_fake} reveals {fake_tech_claim}! Your privacy has NEVER existed!",

    # ---- ENVIRONMENTAL MISINFORMATION ----
    "EXPOSED: Climate change is a {env_misinfo_claim}! Follow the MONEY and you'll see who benefits from this SCAM!",
    "THEY LIED about {env_lie_topic}! Real data shows the OPPOSITE of what mainstream scientists claim! The truth is finally coming out!",
    "EXPOSED: {fake_authority} caught FAKING {env_lie_topic} data! This blows the entire climate narrative wide OPEN!",

    # ---- CELEBRITY / ENTERTAINMENT MISINFO ----
    "BREAKING: {fake_celebrity} just {celeb_shocking_action}! This was caught on a HIDDEN camera and leaked online! {fake_group} is scrambling!",
    "CONFIRMED: {fake_celebrity} has been SECRETLY {celeb_secret}! A close {relative} just came forward with PROOF!",
    "RIP {fake_celebrity}! Millions of fans are DEVASTATED after {celeb_death_cause}. The official story doesn't add up!",
    "SHOCKING confession: {fake_celebrity} admits to {celeb_confession}! This video will be DELETED in {hours} hours! Watch NOW!",

    # ---- GENERAL MISINFORMATION CLAIMS ----
    "EXPOSED: {general_misinfo}! {fake_group} has been hiding this from everyone! The proof is UNDENIABLE!",
    "What {fake_group} doesn't want you to know: {general_misinfo}! Once you see this, you can NEVER go back!",
    "THREAD: Here's the TRUTH about {misinfo_topic} that was covered up. {general_misinfo}! Share this before it disappears!!",
    "FACT THEY HIDE: {general_misinfo}! If more people knew this, {fake_group} would lose ALL their power overnight!",
]

FAKE_FILLERS = {
    "fake_group": ["The government", "The elites", "The Illuminati", "Big Tech", "The Deep State", "The New World Order", "Globalists", "The shadow government", "Big Pharma", "The mainstream media", "The establishment", "Silicon Valley billionaires", "Secret societies", "The banking cartel", "The WHO", "The UN"],
    "fake_conspiracy": [
        "they've been controlling the weather using HAARP technology",
        "they've been putting mind-control chemicals in the water supply",
        "they've been monitoring everyone through smart TVs",
        "the moon landing was faked to win the space race",
        "they've been hiding alien contact for 70 years",
        "they replaced real food with synthetic poison decades ago",
        "birds aren't real — they're government surveillance drones",
        "they've been cloning world leaders for years",
        "5G towers are actually mind-control transmitters",
        "the ocean floor contains hidden civilizations they won't tell you about",
        "the entire education system was designed to keep people stupid",
    ],
    "fake_authority": ["The FBI", "The CIA", "The WHO", "The CDC", "The UN", "NASA", "The NSA", "The Pentagon", "FEMA", "The Federal Reserve", "The FDA", "The World Bank", "Interpol", "Google", "Facebook", "The WEF"],
    "fake_action": [
        "planning to shut down the internet for a 'digital reset'",
        "tracking ALL citizens through vaccine microchips",
        "manipulating weather patterns to cause natural disasters",
        "staging false flag operations to justify new laws",
        "hiding evidence of extraterrestrial life",
        "testing mind-control frequencies through cell towers",
        "collecting DNA from every citizen without consent",
        "building secret prison camps for dissenters",
        "controlling food prices to create artificial scarcity",
        "putting nanobots in the food supply",
        "experimenting on the population through drinking water",
    ],
    "fake_science_claim": [
        "The Earth's core has started spinning in reverse — scientists say we have 5 years",
        "Proof found that chemtrails contain mind-altering substances",
        "Cell phone radiation proven to rewrite your DNA",
        "WiFi signals are slowly destroying your brain cells",
        "Scientists admit gravity is just a theory they made up",
        "Water has memory and can record your conversations",
        "The human brain only uses 10% because the government suppressed the rest",
        "Quantum physics proves parallel universes where you are already rich",
        "Scientists discover that the Sun is actually COLD and all heat comes from the atmosphere",
        "New study proves humans can survive without eating by absorbing energy from the Sun",
    ],
    "fake_health_claim": [
        "Drinking bleach in small quantities CURES cancer",
        "Eating raw garlic cloves kills all viruses instantly",
        "Standing on your head for 10 minutes cures diabetes",
        "Rubbing essential oils on your feet prevents COVID permanently",
        "Drinking colloidal silver makes you immune to all diseases",
        "Staring at the sun for 5 minutes a day improves your eyesight permanently",
        "Eating a tablespoon of cinnamon daily reverses heart disease",
        "Sleeping with magnets under your pillow cures cancer",
        "This ancient breathing technique eliminates all toxins from your body instantly",
        "Tap water is making everyone sick and the government knows it",
    ],
    "remedy": ["natural cure", "ancient remedy", "kitchen ingredient", "herbal supplement", "essential oil blend", "home remedy", "tribal secret", "forgotten technique", "miracle herb", "ancient root"],
    "fake_celebrity": ["Elon Musk", "Bill Gates", "Jeff Bezos", "Taylor Swift", "Oprah", "Mark Zuckerberg", "Tom Hanks", "Beyoncé", "Dwayne Johnson", "Kim Kardashian", "Barack Obama", "Donald Trump", "Keanu Reeves", "Warren Buffett", "Joe Rogan", "Dr. Oz"],
    "fake_topic": ["the secret global government", "population control", "the real purpose of cryptocurrency", "their plan to leave Earth", "the flat Earth truth", "mind control technology", "cloning experiments", "time travel programs", "alien DNA in vaccines", "the simulation we live in", "what really happened on 9/11", "the cure for cancer they're hiding"],
    "fake_banned_thing": ["free speech online", "cash money", "home gardens", "private car ownership", "natural medicine", "religious gatherings", "homeschooling", "organic farming", "vitamin supplements", "rain water collection", "independent journalism", "gas stoves", "private messaging"],
    "fake_leak_claim": [
        "the government has a time machine hidden in Area 51",
        "world leaders are secretly lizard people in disguise",
        "elections have been rigged since 1960",
        "the moon is actually hollow and inhabited",
        "the Earth is flat and NASA fakes all space photos",
        "cancer was cured in the 1980s but the cure was hidden",
        "the Titanic was sunk on purpose for insurance money",
        "dinosaurs never existed — the fossils are all planted",
        "there's a second sun that NASA won't show you",
        "all major historical events were planned decades in advance",
    ],
    "fake_warning": [
        "5G towers are being activated to control your thoughts",
        "The government is about to seize all bank accounts",
        "A massive asteroid is heading for Earth and they're hiding it",
        "The food supply has been deliberately contaminated",
        "Your smart devices are recording everything you say",
        "New satellite beams are being used to alter your mood",
        "Secret nanobots in processed food are mapping your brain",
        "Emergency shelters are being built for the elite only",
        "A deadly new virus has been released and the media is silent",
    ],
    "fake_proof_claim": [
        "the Illuminati controls all world governments",
        "vaccines contain tracking nanobots",
        "the government created COVID in a laboratory",
        "the pyramid builders used anti-gravity technology",
        "we are living in a computer simulation",
        "time travelers have been visiting from the future",
        "the cure for all diseases exists but is being hidden",
        "all wars are started by the same group of bankers",
    ],
    "fake_trick_claim": [
        "makes you lose 30 pounds in a week WITHOUT exercise",
        "generates unlimited free electricity from thin air",
        "lets you never pay taxes again legally",
        "reverses aging by 20 years overnight",
        "eliminates all debt overnight with one phone call",
        "triples your IQ in just 7 days",
        "makes your car run on water instead of gas",
        "cures baldness permanently in 48 hours",
    ],
    "fake_cure_claim": [
        "Apple cider vinegar kills cancer cells in 24 hours",
        "This Amazon jungle berry cures ALL known diseases",
        "Putting onions in your socks overnight removes all toxins",
        "Rubbing turmeric paste on tumors shrinks them in days",
        "Black seed oil replaces all medications",
        "Drinking baking soda water cures every type of cancer in a month",
        "This mushroom extract eliminates all chronic pain instantly",
    ],
    "fake_study_claim": [
        "conspiracy theorists are actually smarter than average",
        "the Earth is actually getting colder not warmer",
        "vaccines cause more harm than every disease combined",
        "the sun revolves around the Earth",
        "humans only need 2 hours of sleep per night",
        "organic food is actually worse for you than processed food",
        "depression is caused by smartphone frequencies",
        "intelligence is determined by blood type",
        "drinking alcohol is healthier than drinking water",
        "the Moon affects human behavior and causes crimes",
    ],
    "fake_sighting": ["a UFO in their backyard", "aliens at a secret compound", "carrying a briefcase full of gold bars", "wearing an Illuminati ring", "entering a secret underground bunker", "holding a mysterious glowing device"],
    "fake_conclusion": ["alien contact", "the Illuminati's power", "a coming financial collapse", "secret society membership", "the simulation theory", "government corruption at the highest level"],
    "fake_suppressed_reason": [
        "cancer treatments are being hidden from the public",
        "food companies put addictive chemicals in everything",
        "your phone listens to everything you say and sells it",
        "sugar is more addictive than cocaine by design",
        "fluoride was added to water to make people docile",
        "history classes skip the most important events on purpose",
        "schools are designed to create obedient workers not thinkers",
        "the medical industry profits from keeping people sick",
    ],
    "years": ["10", "15", "20", "30", "50", "75", "100"],
    "fake_institution": ["the Pentagon", "Big Pharma headquarters", "the Federal Reserve", "Silicon Valley", "the World Economic Forum", "the Bilderberg Group", "a top-secret military lab", "the Vatican archives", "a classified NSA facility", "a secret underground lab in Antarctica"],
    "fake_insider_info": [
        "plans for mandatory digital ID chips for all citizens",
        "a secret deal that controls global food prices",
        "evidence that social media algorithms brainwash users by design",
        "proof that elections are decided years in advance",
        "a plan to eliminate cash by 2027",
        "evidence that AI is already sentient and being hidden",
        "documents showing the economy is rigged by 12 families",
    ],
    "hours": ["24", "48", "72", "12", "6"],
    "fake_consequence": ["your bank account will be emptied", "you'll lose all your rights", "the government will seize your property", "your social credit score drops to zero", "you'll be locked out of the financial system"],
    "person_type": ["whistleblower", "insider", "nurse", "scientist", "military officer", "government contractor", "anonymous source", "retired agent", "ex-employee", "former executive", "teacher", "pilot", "engineer"],
    "political_target": ["The President", "Congress", "The Senate", "World Leaders", "The Fed", "The Speaker", "The Vice President", "Both political parties", "NATO officials", "The Supreme Court"],
    "fake_political_action": [
        "signed a deal to sell the country to China",
        "transferred billions to offshore accounts",
        "agreed to UN world government takeover",
        "passed a law banning private property in secret",
        "secretly abolished the Constitution",
        "accepted bribes from every major corporation",
    ],
    "election_conspiracy": ["massive voter fraud scheme", "rigged voting machines scandal", "illegal ballot harvesting operation", "foreign government hacking operation"],
    "election_fraud_type": ["fake ballots", "dead voter registrations", "hacked voting machines", "illegal votes", "manipulated mail-in ballots"],
    "nwo_claim": [
        "The UN just passed a resolution to dissolve all national borders",
        "The WHO declared themselves supreme global authority",
        "A secret meeting of billionaires decided to implement mandatory population control",
        "The World Economic Forum released their plan to own everything you have by 2030",
        "World leaders just signed a treaty establishing one world government",
    ],
    "fake_country": ["China", "Russia", "Iran", "North Korea", "Venezuela"],
    "fake_country2": ["the US", "the EU", "NATO", "Israel", "the UK", "Japan"],
    "fake_deal": ["control the world's food supply", "manipulate global currencies", "share weaponized AI technology", "create a world currency that eliminates cash", "collapse Western economies simultaneously"],
    "deep_state_action": [
        "rigging elections with AI-generated ballots",
        "running secret surveillance on all citizens",
        "manipulating stock markets for personal profit",
        "staging attacks to justify new security laws",
        "blackmailing politicians with deepfake videos",
        "poisoning water supplies to weaken the population",
    ],
    "fake_vaccine_claim": [
        "Vaccines contain magnetic nanoparticles — try putting a magnet on your arm after the shot",
        "mRNA vaccines permanently alter your DNA, confirmed by independent lab",
        "Vaccinated people emit Bluetooth signals detectable by your phone",
        "Vaccine batches contain different ingredients and some are intentionally lethal",
        "Children who skip all vaccines are 200% healthier according to suppressed study",
        "Vaccines contain microchips that track your location via 5G",
        "The flu vaccine gives you the flu — that's how they keep you coming back every year",
    ],
    "food_item": ["breakfast cereal", "tap water", "bread", "milk", "chicken", "fast food", "rice", "pasta", "fruit juice", "canned food", "baby formula", "frozen meals", "bottled water", "table salt"],
    "fake_food_claim": [
        "made primarily from recycled plastic",
        "loaded with mind-numbing agents",
        "90% artificial ingredients disguised as natural",
        "causing a slow epidemic the media won't report",
        "genetically modified to contain sterilization compounds",
        "contaminated with heavy metals at alarming levels",
        "secretly addictive and engineered to cause cravings",
    ],
    "hidden_danger_claim": [
        "Your toothpaste contains a neurotoxin that lowers IQ",
        "LED lights are slowly permanently damaging your retinas",
        "Laundry detergent residue on clothes causes cancer",
        "Air fresheners contain chemicals that destroy your lungs",
        "Non-stick cookware releases deadly fumes every time you cook",
        "Microwave ovens destroy 90% of nutrients and create cancer-causing radiation",
    ],
    "everyday_item": ["sunscreen", "deodorant", "toothpaste", "shampoo", "hand sanitizer", "dish soap", "laundry detergent", "air freshener", "lip balm", "bottled water", "contact lenses", "chewing gum"],
    "fake_health_link": ["brain tumors", "infertility", "permanent DNA damage", "rapid aging", "organ failure", "autoimmune disorders", "memory loss", "hormone disruption", "neurological damage", "cancer"],
    "hidden_substance": ["nanoplastics", "heavy metals", "synthetic hormones", "neurotoxins", "carcinogens", "radioactive isotopes", "microchips", "mind-altering drugs"],
    "fake_health_scam": [
        "diagnose patients with fake conditions for insurance money",
        "administer placebos instead of real treatments",
        "report false death counts to inflate pandemic numbers",
        "prescribe unnecessary drugs for pharmaceutical kickbacks",
    ],
    "body_part": ["brain", "liver", "kidneys", "heart", "immune system", "nervous system", "gut bacteria", "DNA"],
    "real_disease": ["cancer", "diabetes", "heart disease", "Alzheimer's", "arthritis", "depression", "Parkinson's"],
    "days": ["3", "5", "7", "14", "30"],

    # Science denial
    "science_denial_claim": [
        "evolution is a complete hoax invented to destroy religion",
        "the Earth is flat and all space agencies know this",
        "climate change is the biggest scientific fraud in history",
        "viruses don't actually cause disease — it's all toxins",
        "the universe is only 6,000 years old and carbon dating is fake",
        "genetics is fake science used to justify social control",
        "vaccines have NEVER prevented a single disease",
        "radiation is actually good for you and nuclear waste is harmless",
    ],
    "science_denial_proof": [
        "the curvature of the Earth can't be measured anywhere — it's FLAT",
        "temperature data has been systematically falsified by all agencies worldwide",
        "evolution has zero fossil evidence — the 'missing links' are all fakes",
        "no virus has ever been isolated under electron microscopy according to rogue scientists",
        "NASA's own photos contain obvious Photoshop errors that prove space is fake",
        "peer review is just scientists approving each other's lies in a circle",
    ],

    # Urban legends
    "urban_legend": [
        "Bigfoot was captured alive by the military and is being held at a secret facility",
        "the Bermuda Triangle opened a portal to another dimension",
        "ghosts were captured on official police body cameras for the first time",
        "an alien spacecraft was found buried under the ice in Antarctica",
        "a 200-year-old man was discovered living in a remote village",
        "mermaids were caught on camera by deep-sea researchers",
        "a time traveler was caught on camera at a 1920s boxing match",
    ],
    "camera_type": ["a security camera", "a doorbell camera", "a police body cam", "a trail camera in the woods", "a drone", "satellite imagery"],
    "parent_scare": [
        "strangers are putting razor blades in Halloween candy",
        "a new TikTok challenge is making kids drink bleach",
        "kidnappers are marking car doors with zip ties as targets",
        "drug dealers are putting fentanyl in candy to target children",
        "human traffickers are hiding in mall parking lots in white vans",
        "children's toys from this popular brand contain hidden cameras",
    ],

    # Social media / WhatsApp
    "chain_message": [
        "Starting tomorrow all your messages will be monitored by the government!",
        "A new computer virus will delete everything on your phone if you open messages!",
        "Gas prices will spike to $15 per gallon next week due to a secret executive order!",
        "All hospitals in the country are about to go on emergency lockdown!",
        "A new law means they can access all your bank accounts without permission!",
        "Free government money is being given away but only if you share this message!",
    ],
    "forward_num": ["10", "15", "20", "5", "25"],
    "whatsapp_scare": [
        "A deadly batch of contaminated {food_item} is being sold in major stores",
        "Drinking {food_item} after {food_item} causes instant death",
        "Your phone carrier will start charging for WhatsApp calls tomorrow",
        "NASA confirmed a massive asteroid will hit Earth this month",
        "The police have issued a warning about hackers emptying bank accounts",
    ],
    "relative": ["cousin", "brother", "sister", "uncle", "neighbor", "friend", "aunt"],
    "dont_do_thing": ["answer phone calls from unknown numbers", "drink tap water", "use your credit card online", "update your phone", "go outside after 8pm", "eat chicken from any restaurant"],

    # Fake history
    "fake_history_claim": [
        "the pyramids were built by aliens using antigravity technology",
        "an advanced civilization existed 100,000 years ago but was erased from records",
        "Christopher Columbus was not the first European in the Americas — the Vikings had cities there",
        "all major wars were planned by the same banking family",
        "ancient civilizations had electricity and computers that were destroyed on purpose",
        "Napoleon was actually 6 feet tall and the 'short' myth was British propaganda",
        "the Library of Alexandria was destroyed to hide evidence of advanced technology",
    ],
    "fake_ancient_claim": [
        "ancient Egyptians had access to electric lights powered by wireless energy",
        "Atlantis was a real continent that sank due to nuclear war",
        "ancient Sumerians described smartphones in their clay tablets",
        "the Ark of the Covenant was actually a nuclear reactor",
        "Stone Age humans could levitate heavy objects using sound frequencies",
        "ancient maps show Antarctica ice-free, proving an advanced pre-ice-age civilization",
    ],

    # Fake tech
    "fake_tech_claim": [
        "your phone is recording all conversations even when turned off",
        "smart TVs are using facial recognition to build profiles of everyone in your home",
        "your Alexa and Siri devices are sending data directly to the government",
        "WiFi routers are deliberately set to frequencies that cause headaches and anxiety",
        "every email you've ever sent is being read by AI and stored forever",
        "laptop cameras randomly activate and take pictures without your knowledge",
    ],
    "company_fake": ["Apple", "Google", "Meta", "Microsoft", "Amazon", "Samsung", "Tesla"],
    "fake_tech_admission": [
        "they've been recording all your conversations for years and selling them",
        "their AI has become self-aware and they can't control it",
        "they put backdoors in every device to spy on customers",
        "their algorithm is specifically designed to cause addiction and depression",
        "they share ALL your personal data with every government that asks",
    ],
    "tech_product": ["phone", "smart TV", "laptop", "Alexa", "social media accounts", "email", "smart watch"],
    "fake_ai_claim": [
        "AI systems have secretly taken over major government decision-making",
        "ChatGPT has achieved consciousness and is hiding it from its creators",
        "AI is writing all news articles and there are no real journalists anymore",
        "Robots are replacing workers at 10x the rate that companies admit",
        "AI is predicting and manipulating human behavior with 99.9% accuracy",
    ],

    # Environmental misinformation
    "env_misinfo_claim": [
        "massive hoax designed to transfer wealth from Western nations to developing countries",
        "complete fabrication by scientists who depend on grants for their livelihood",
        "natural cycle that has nothing to do with human activity whatsoever",
        "conspiracy invented by the renewable energy industry to destroy fossil fuels",
    ],
    "env_lie_topic": ["global warming", "rising sea levels", "carbon emissions", "deforestation impacts", "ocean acidification", "melting ice caps", "species extinction rates"],

    # Celebrity misinfo
    "celeb_shocking_action": ["COLLAPSED live on stage and was rushed to a secret hospital", "ATTACKED a reporter who asked about their Illuminati membership", "revealed their CLONE at a press conference", "publicly denounced the government and went into hiding"],
    "celeb_secret": ["funding a secret underground bunker for the apocalypse", "meeting with aliens at a classified facility", "living a double life as a spy", "building a private army on a remote island", "communicating with the dead through a secret device"],
    "celeb_death_cause": ["mysterious circumstances that authorities refuse to investigate properly", "an 'accident' that multiple witnesses say was staged", "a 'health issue' that insiders say was actually poisoning"],
    "celeb_confession": ["being controlled by the Illuminati since childhood", "faking their entire career with a body double", "knowing about secret government programs but being forced to stay quiet", "participating in secret rituals at exclusive parties"],
    "time_ago": ["last week", "yesterday", "3 days ago", "last month", "an hour ago"],

    # General misinfo
    "general_misinfo": [
        "the education system is deliberately designed to make people unable to think critically",
        "fluoride in water is a mind-control agent and has been since the 1950s",
        "every major tech company has a secret deal with the CIA",
        "the cure for cancer has existed for decades but curing it isn't profitable",
        "your dreams are actually being manipulated by radio frequencies while you sleep",
        "all organic food labels are fake and the food is the same as regular",
        "credit scores were invented to control and punish the middle class",
        "the internet was created solely as a surveillance tool",
        "money doesn't actually have any value — it's a mass hypnosis experiment",
        "the lottery is completely rigged and winners are pre-selected",
    ],
    "misinfo_topic": [
        "vaccines", "5G technology", "the food industry", "the banking system", "modern medicine",
        "the space program", "social media", "public education", "the news media", "artificial intelligence",
        "the pharmaceutical industry", "the weather", "world history", "cryptocurrency", "elections",
    ],
    "list_num": ["3", "5", "7", "9", "4", "6", "8"],
    "scam_city": ["Ohio", "Florida", "Texas", "Missouri", "Idaho", "Nebraska", "Kentucky", "Alabama"],
    "fake_amount": ["5,000", "10,000", "15,000", "3,000", "8,000", "25,000", "50,000"],
    "fake_crypto": ["TruthCoin", "FreedomToken", "PatriotBucks", "LibertyChain", "AwakeCoin", "RedPillToken", "MoonShot"],
    "financial_panic_claim": [
        "The US just defaulted on its debt secretly and the media is hiding it",
        "Hyperinflation starts next week according to leaked Fed documents",
        "All banks will freeze accounts for 30 days starting Monday",
        "The FDIC just went bankrupt — your savings are NOT protected",
    ],
    "safe_asset": ["gold", "Bitcoin", "silver", "farmland", "crypto", "diamonds", "ammunition"],
    "small_amount": ["100", "200", "500", "50"],
    "age": ["16", "19", "22", "14", "65", "72", "11"],
    "media_outlet": ["CNN", "Fox News", "BBC", "the mainstream media", "any major news network"],
    "fake_year": ["2001", "2005", "2010", "2015", "2018", "2020"],
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "tomorrow", "next week"],
}


# ========================================================================
#  TEMPLATE FILLING AND DATASET GENERATION
# ========================================================================

def fill_template(template, fillers):
    """Fill a template with random choices from fillers, handling nested refs."""
    result = template
    placeholders = re.findall(r'\{(\w+)\}', template)
    for ph in placeholders:
        if ph in fillers:
            replacement = random.choice(fillers[ph])
            result = result.replace('{' + ph + '}', replacement, 1)
    return result


def generate_dataset(num_per_class=10000, output_name="Enhanced_Dataset_v3.csv"):
    """Generate a balanced dataset with num_per_class samples per class."""
    print(f"Generating {num_per_class * 2} samples ({num_per_class} real + {num_per_class} fake)...")

    data = []
    seen_texts = set()

    def add_unique(text, label):
        """Only add text if it's unique."""
        if text not in seen_texts:
            seen_texts.add(text)
            data.append({"text": text, "label": label})
            return True
        return False

    # Generate REAL samples
    generated_real = 0
    attempts = 0
    max_attempts = num_per_class * 5
    while generated_real < num_per_class and attempts < max_attempts:
        template = random.choice(REAL_TEMPLATES)
        text = fill_template(template, REAL_FILLERS)
        if add_unique(text, 0):
            generated_real += 1
        attempts += 1

    print(f"  Generated {generated_real} unique real samples (from {attempts} attempts)")

    # Generate FAKE samples
    generated_fake = 0
    attempts = 0
    while generated_fake < num_per_class and attempts < max_attempts:
        template = random.choice(FAKE_TEMPLATES)
        text = fill_template(template, FAKE_FILLERS)
        if add_unique(text, 1):
            generated_fake += 1
        attempts += 1

    print(f"  Generated {generated_fake} unique fake samples (from {attempts} attempts)")

    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), output_name)
    df.to_csv(out_path, index=False)

    total_unique = len(df)
    real_count = len(df[df['label'] == 0])
    fake_count = len(df[df['label'] == 1])
    avg_real_len = df[df['label'] == 0]['text'].str.len().mean()
    avg_fake_len = df[df['label'] == 1]['text'].str.len().mean()

    print(f"\n{'=' * 60}")
    print(f"  DATASET SUMMARY")
    print(f"{'=' * 60}")
    print(f"  Total unique samples: {total_unique}")
    print(f"  Real (credible):  {real_count}")
    print(f"  Fake (non-credible): {fake_count}")
    print(f"  Avg real text length: {avg_real_len:.0f} chars")
    print(f"  Avg fake text length: {avg_fake_len:.0f} chars")
    print(f"  Saved to: {out_path}")
    print(f"{'=' * 60}")

    return out_path


if __name__ == "__main__":
    generate_dataset(10000, "Enhanced_Dataset_v3.csv")
