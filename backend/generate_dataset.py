"""
Enhanced Fake News Dataset Generator
Creates a large, diverse dataset with realistic news patterns for training.
"""

import pandas as pd
import random
import os

random.seed(42)

# ============================================================
# REAL NEWS TEMPLATES — factual, measured language, credible
# ============================================================

REAL_TEMPLATES = [
    # Economy / Finance
    "The Federal Reserve announced a {rate}% interest rate {direction} on {day}, citing {economic_reason}. Economists {reaction} the decision, noting its potential impact on {sector}.",
    "According to the Bureau of Labor Statistics, the unemployment rate {moved} to {pct}% in {month}, {beating_missing} analysts' expectations of {pct2}%.",
    "The stock market {rose_fell} {points} points on {day} as investors reacted to {market_catalyst}. The S&P 500 closed at {sp_val}.",
    "GDP growth for {quarter} came in at {gdp_pct}%, {above_below} the {gdp_pct2}% forecast, according to data released by the Commerce Department.",
    "{company} reported quarterly earnings of ${earnings} per share, {beating_missing} Wall Street estimates by {cents} cents. Revenue came in at ${revenue} billion.",
    "New data from the International Monetary Fund shows global economic growth is projected at {gdp_pct}% for {year}, {direction2} from {gdp_pct2}% the previous year.",

    # Politics — neutral, factual
    "President {president} signed {bill_name} into law on {day}, a measure that {bill_desc}. The legislation passed with bipartisan support in {chamber}.",
    "The {chamber} voted {vote_for}-{vote_against} to approve {bill_name}, which would {bill_desc}. The bill now heads to {next_chamber} for consideration.",
    "Secretary of State {official} met with {foreign_leader} in {city} to discuss {diplomatic_topic}. Both sides described the talks as productive.",
    "The Supreme Court agreed to hear arguments in {case_name}, a case concerning {legal_topic}. Oral arguments are scheduled for {month}.",
    "Voter turnout in the {state} {election_type} reached {turnout_pct}%, according to the state's election commission, {up_down} from {turnout_pct2}% in the previous cycle.",
    "A bipartisan committee released its report on {policy_topic}, recommending {num_recs} changes to existing regulations. Committee members noted broad agreement on key points.",

    # Science / Technology
    "Researchers at {university} published a study in {journal} showing that {science_finding}. The study involved {num_participants} participants over {study_period}.",
    "NASA announced the successful launch of {mission_name} from {launch_site} on {day}. The spacecraft is expected to reach {destination} in approximately {travel_time}.",
    "A team of scientists from {institution} discovered {discovery}, according to findings published in {journal}. The research could lead to advances in {field}.",
    "The World Health Organization reported that global cases of {disease} {rose_fell2} by {pct}% compared to the previous {time_period}, attributing the change to {health_reason}.",
    "Climate data from {source_org} indicates that the global average temperature in {year} was {temp_change} degrees above the pre-industrial baseline, continuing a long-term warming trend.",
    "A new peer-reviewed study in {journal} found that {health_finding}. Researchers emphasized the need for further investigation before drawing clinical conclusions.",

    # Everyday / Human Interest
    "City officials in {city} approved a ${amount} million plan to {city_project}. Construction is expected to begin in {month} and be completed by {year}.",
    "The local school district announced plans to {education_plan}, affecting approximately {num_students} students across {num_schools} schools. Parents have been invited to comment at upcoming board meetings.",
    "Transit authorities approved expanded service on the {transit_line} line, adding {num_trains} additional trains during peak hours starting {month}.",
    "A wildfire in {state} has burned approximately {acres} acres as of {day}, with firefighters reporting {containment_pct}% containment. No fatalities have been reported.",
    "The {sports_team} defeated the {opponent} {score} in {event}, securing their place in the {round}. Coach {coach_name} praised the team's defensive effort.",
    "Severe weather warnings were issued for {region} on {day} as meteorologists tracked a {weather_system} expected to bring {weather_impact}.",
]

REAL_FILLERS = {
    "rate": ["0.25", "0.50", "0.75"],
    "direction": ["increase", "decrease", "hold"],
    "day": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"],
    "economic_reason": ["persistent inflation concerns", "slowing economic growth", "strong labor market data", "easing supply chain pressures"],
    "reaction": ["largely supported", "debated the merits of", "expressed mixed views on", "cautiously welcomed"],
    "sector": ["housing", "consumer spending", "small businesses", "international trade"],
    "moved": ["dropped", "rose", "remained steady", "fell slightly"],
    "pct": ["3.4", "3.7", "4.1", "3.9", "5.2", "4.8"],
    "pct2": ["3.5", "3.8", "4.0", "4.2", "5.0", "4.6"],
    "month": ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"],
    "beating_missing": ["beating", "missing", "matching"],
    "rose_fell": ["rose", "fell", "gained", "lost"],
    "points": ["150", "212", "85", "310", "47", "523", "198"],
    "market_catalyst": ["better-than-expected earnings reports", "new trade deal announcements", "inflation data", "oil price fluctuations", "tech sector performance"],
    "sp_val": ["4,523", "5,012", "4,890", "5,134", "4,678"],
    "quarter": ["Q1 2025", "Q2 2025", "Q3 2024", "Q4 2024", "Q1 2026"],
    "gdp_pct": ["2.1", "1.8", "3.2", "2.5", "2.9", "1.4"],
    "gdp_pct2": ["2.0", "1.9", "3.0", "2.3", "2.7", "1.6"],
    "above_below": ["above", "below", "in line with"],
    "company": ["Apple", "Microsoft", "Amazon", "Google", "Tesla", "Meta", "Johnson & Johnson", "Pfizer", "Toyota", "Samsung"],
    "earnings": ["1.52", "2.13", "0.98", "3.45", "1.87", "2.76"],
    "cents": ["3", "7", "12", "5", "2"],
    "revenue": ["24.5", "18.3", "32.1", "7.8", "12.4", "45.6"],
    "year": ["2024", "2025", "2026"],
    "direction2": ["up", "down", "unchanged"],
    "president": ["the President", "Biden", "the administration"],
    "bill_name": ["the Infrastructure Investment Act", "the Education Modernization Act", "the Clean Energy Transition Act", "a new defense spending authorization", "the Healthcare Access Act"],
    "bill_desc": ["allocates funding for bridge and road repairs", "expands access to early education programs", "provides tax incentives for renewable energy", "modernizes cybersecurity protocols across federal agencies", "extends insurance coverage options"],
    "chamber": ["the Senate", "the House of Representatives", "Congress"],
    "next_chamber": ["the Senate", "the House"],
    "vote_for": ["67", "54", "72", "231", "218", "289"],
    "vote_against": ["33", "46", "28", "198", "212", "143"],
    "official": ["Blinken", "the Secretary", "Sullivan"],
    "foreign_leader": ["foreign dignitaries", "regional leaders", "EU officials", "NATO allies"],
    "city": ["Washington", "Geneva", "Tokyo", "London", "Brussels", "Seoul", "Beijing", "Austin", "Denver", "Portland"],
    "diplomatic_topic": ["trade agreements", "climate policy coordination", "defense cooperation", "humanitarian aid"],
    "case_name": ["Smith v. United States", "Gonzalez v. State Board", "National Association v. Department"],
    "legal_topic": ["digital privacy rights", "environmental regulations", "interstate commerce", "voting district boundaries"],
    "state": ["California", "Texas", "Florida", "Ohio", "Michigan", "Pennsylvania", "Georgia", "Arizona", "Colorado", "Oregon"],
    "election_type": ["primary", "general election", "special election", "midterm"],
    "turnout_pct": ["62", "58", "71", "45", "67"],
    "turnout_pct2": ["59", "55", "68", "42", "64"],
    "up_down": ["up", "down"],
    "policy_topic": ["immigration reform", "healthcare funding", "education standards", "transportation infrastructure"],
    "num_recs": ["12", "8", "15", "6"],
    "university": ["MIT", "Stanford", "Johns Hopkins", "the University of Oxford", "Harvard", "Caltech", "UC Berkeley"],
    "journal": ["Nature", "Science", "The Lancet", "JAMA", "Cell", "PNAS", "The New England Journal of Medicine"],
    "science_finding": ["a new compound may slow the progression of Alzheimer's disease", "exercise significantly reduces the risk of cardiovascular events in older adults", "microplastics are present in a wider range of food products than previously thought", "a gene therapy approach shows promise in treating sickle cell disease"],
    "num_participants": ["1,200", "5,000", "850", "15,000", "3,400"],
    "study_period": ["3 years", "18 months", "5 years", "10 months"],
    "mission_name": ["the Artemis III mission", "the Mars Sample Return probe", "a new Earth observation satellite", "the Europa Clipper spacecraft"],
    "launch_site": ["Kennedy Space Center", "Vandenberg Space Force Base", "Cape Canaveral"],
    "destination": ["the Moon", "Mars orbit", "Jupiter's moon Europa", "low Earth orbit"],
    "travel_time": ["6 months", "3 days", "2 years", "6 weeks"],
    "institution": ["the Max Planck Institute", "CERN", "the National Institutes of Health", "the Salk Institute"],
    "discovery": ["a new species of deep-sea organism", "a potential biomarker for early cancer detection", "evidence of ancient water on Mars", "a novel approach to quantum error correction"],
    "field": ["oncology", "marine biology", "planetary science", "quantum computing", "materials science"],
    "disease": ["malaria", "tuberculosis", "measles", "dengue fever"],
    "rose_fell2": ["decreased", "increased", "remained stable"],
    "time_period": ["year", "quarter", "month"],
    "health_reason": ["expanded vaccination programs", "seasonal factors", "improved diagnostic capabilities", "public health interventions"],
    "source_org": ["NOAA", "the European Space Agency", "the World Meteorological Organization"],
    "temp_change": ["1.2", "1.1", "1.3", "1.48"],
    "health_finding": ["moderate coffee consumption is associated with a lower risk of type 2 diabetes", "regular sleep schedules improve cognitive performance in children", "air pollution exposure may increase the risk of respiratory infections"],
    "amount": ["45", "120", "200", "78", "15"],
    "city_project": ["renovate the downtown transit hub", "build a new community recreation center", "expand the water treatment facility", "upgrade public school buildings"],
    "education_plan": ["introduce a revised STEM curriculum", "hire 200 additional teachers", "expand after-school tutoring programs"],
    "num_students": ["12,000", "8,500", "25,000", "5,000"],
    "num_schools": ["18", "24", "35", "12"],
    "transit_line": ["Blue", "Red", "Green", "Orange"],
    "num_trains": ["6", "10", "8", "12"],
    "acres": ["3,500", "12,000", "800", "25,000"],
    "containment_pct": ["35", "60", "85", "15", "50"],
    "sports_team": ["Lakers", "Barcelona", "Yankees", "Patriots", "Warriors"],
    "opponent": ["Celtics", "Real Madrid", "Red Sox", "Bills", "Nuggets"],
    "score": ["3-1", "102-98", "4-2", "24-17", "2-0"],
    "event": ["last night's game", "Sunday's match", "the championship series"],
    "round": ["semifinals", "finals", "next round of playoffs"],
    "coach_name": ["Smith", "Johnson", "Williams", "Rodriguez", "Thompson"],
    "region": ["the Gulf Coast", "the Pacific Northwest", "the Midwest", "the Northeast", "the Southwest"],
    "weather_system": ["tropical storm", "cold front", "low-pressure system", "severe thunderstorm complex"],
    "weather_impact": ["heavy rainfall and possible flooding", "high winds and below-freezing temperatures", "hail and damaging wind gusts", "significant snowfall accumulations"],
}

# ============================================================
# FAKE NEWS TEMPLATES — sensational, conspiratorial, clickbait
# ============================================================

FAKE_TEMPLATES = [
    # Conspiracy / Alarmist
    "BREAKING: {fake_group} caught in massive cover-up — {fake_conspiracy}!! They don't want you to know this! Share before it's deleted!!!",
    "EXPOSED: {fake_authority} secretly {fake_action}. Whistleblower reveals SHOCKING truth that changes EVERYTHING you thought you knew!",
    "Scientists STUNNED: {fake_science_claim}! Big Pharma has been HIDING this from the public for decades. The truth is finally out!",
    "URGENT: {fake_health_claim}! Doctors are BAFFLED. This simple {remedy} has been suppressed by the medical establishment for years.",
    "You WON'T BELIEVE what {fake_celebrity} just said about {fake_topic}! The internet is going CRAZY after this revelation!",
    "{fake_group} just BANNED {fake_banned_thing}! This is the beginning of the end of freedom as we know it!!!",
    "LEAKED document proves {fake_leak_claim}! The government has been lying to us for YEARS. Wake up people!!!",
    "WARNING: {fake_warning}. The mainstream media is covering this up. Spread this NOW before they take it down!",
    "PROOF that {fake_proof_claim}! Top insider finally breaks silence and reveals what's REALLY going on behind closed doors!",
    "JUST IN: {fake_financial_scam}. Thousands of ordinary people already made millions! Experts are FURIOUS that this secret is out!",
    "TOP SECRET: {fake_authority} has been {fake_action} for {years} years and {person_type} just confirmed it!! The TRUTH is finally coming out!",
    "WAKE UP SHEEPLE: {fake_conspiracy}!! This is NOT a conspiracy theory anymore — {fake_group} has been caught red-handed!!!",
    "ALERT! {fake_warning}!! This is being CENSORED by {fake_group}! Repost this on every platform before they shut us down!",
    "CONFIRMED: {fake_authority} insider admits {fake_leak_claim}! This is the BOMBSHELL that will bring down the entire system!",
    "HAPPENING NOW: {fake_group} is {fake_action}! Multiple {person_type} have verified this! Why is NO ONE talking about this?!",

    # Clickbait / Misleading
    "This one weird trick {fake_trick_claim}. Doctors HATE it! Number 7 will shock you!",
    "MIRACLE cure discovered: {fake_cure_claim}. Why isn't the media reporting on this?? Big Pharma doesn't want you to see this!",
    "Study PROVES that {fake_study_claim}. The results are MIND-BLOWING and will change everything you thought was true!",
    "{fake_celebrity} spotted with {fake_sighting}! Fans are in COMPLETE SHOCK. Is this proof of {fake_conclusion}??",
    "I tried this {remedy} for 30 days and what happened BLEW MY MIND! The secret {fake_group} doesn't want you to know!",
    "FINALLY: The real reason {fake_suppressed_reason}. This information has been suppressed for {years} years!",
    "Exclusive: Anonymous source inside {fake_institution} reveals {fake_insider_info}. This changes EVERYTHING!",
    "You have {hours} hours to do THIS or {fake_consequence}! The government won't tell you about this loophole!",
    "After {years} years of silence a former {person_type} just confessed: {fake_suppressed_reason}. The truth can no longer be hidden!!!",
    "What {fake_celebrity} did {time_ago} SHOOK the entire world! You need to see this before {fake_group} takes it down!",
    "{person_type} exposed the REAL truth about {fake_topic}! The video went viral and {fake_group} is trying desperately to delete it!",
    "Scientists at {fake_institution} just published a FORBIDDEN study proving {fake_study_claim}! The establishment is PANICKING!",
    "TOP 10 things {fake_group} doesn't want you to know about {fake_topic}! Number {list_num} will leave you SPEECHLESS!!!",

    # Political misinformation
    "{political_target} secretly {fake_political_action}! Documents PROVE what we suspected all along! MSM silent on this!",
    "EXPOSED: The {election_conspiracy} during the last election. Millions of {election_fraud_type} confirmed by inside source!",
    "NEW WORLD ORDER: {nwo_claim}. This is NOT a drill. The elite have been planning this for decades!",
    "{fake_country} just made a secret deal with {fake_country2} to {fake_deal}. The media is completely SILENT on this bombshell!",
    "Deep state operatives caught {deep_state_action}. This is the biggest scandal in American history and NO ONE is talking about it!",
    "SHOCKING video shows {political_target} admitting to {fake_political_action}! Why isn't {media_outlet} covering this??",
    "LEAKED emails prove {political_target} has been {deep_state_action} since {fake_year}! The evidence is OVERWHELMING!",
    "URGENT: {political_target} just signed a SECRET executive order to {fake_deal}. Your rights are being STOLEN right now!",
    "We have DEFINITIVE PROOF that the {election_conspiracy}. Share this with everyone you know before it gets censored!",

    # Health misinformation
    "Exposed: {fake_vaccine_claim}! Your doctor WON'T tell you this. Exposed by brave researchers who risked everything!",
    "This common {food_item} is actually {fake_food_claim}! Scientists confirm what conspiracy theorists have been saying for years!",
    "HIDDEN DANGER: {hidden_danger_claim}! The FDA has been covering this up. Watch this video before they ban it!",
    "SECRET ingredient in {everyday_item} linked to {fake_health_link}! You'll NEVER use it again after reading this!",
    "EXPOSED: Hospitals are being PAID to {fake_health_scam}! A brave {person_type} just leaked the internal documents!",
    "The {food_item} you eat every day is DESTROYING your {body_part}! Exposed by rogue scientist who was FIRED for speaking out!",
    "THEY LIED: {fake_vaccine_claim}! Independent lab results prove what millions of people already suspected. The cover-up is OVER!",
    "WARNING: {everyday_item} contains {hidden_substance} that causes {fake_health_link}! Why hasn't the FDA warned us?!",

    # Financial scams
    "BREAKING: Kid from {city} discovers way to make ${fake_amount} per day from home! Banks HATE this one simple trick!",
    "Elon Musk just endorsed {fake_crypto}! Invest now before it goes to the MOON! Limited spots available!!",
    "ALERT: The dollar is about to COLLAPSE! {financial_panic_claim}. Buy {safe_asset} NOW before it's too late!",
    "{fake_celebrity} reveals secret investment that turns ${small_amount} into ${fake_amount} in just {days} days! Banks are TERRIFIED!",
    "SHOCKING: {person_type} accidentally reveals the {safe_asset} loophole that {fake_group} has been hiding! Act NOW!",
    "A {age}-year-old from {city} just made ${fake_amount} in {days} days using this ONE WEIRD {safe_asset} trick! {fake_group} is furious!",
]

FAKE_FILLERS = {
    "fake_group": ["The government", "The elites", "The Illuminati", "Big Tech", "The Deep State", "The New World Order", "Globalists", "The shadow government", "The cabal", "Big Pharma", "The mainstream media", "The establishment", "Silicon Valley billionaires", "Secret societies", "The banking cartel"],
    "fake_conspiracy": ["they've been controlling the weather using HAARP technology", "they've been putting mind-control chemicals in the water supply", "they've been monitoring everyone through smart TVs", "the moon landing was faked to win the space race", "they've been hiding alien contact for 70 years", "they built underground cities for the elite while leaving us to suffer", "they replaced real food with synthetic poison decades ago", "they've been using social media to program your thoughts", "birds aren't real — they're government surveillance drones", "they've been cloning world leaders for years"],
    "fake_authority": ["The FBI", "The CIA", "The WHO", "The CDC", "The UN", "NASA", "The NSA", "The Pentagon", "FEMA", "The Federal Reserve", "The FDA", "The World Bank", "Interpol"],
    "fake_action": ["planning to shut down the internet for a 'digital reset'", "tracking ALL citizens through vaccine microchips", "manipulating weather patterns to cause natural disasters", "staging false flag operations to justify new laws", "hiding evidence of extraterrestrial life", "testing mind-control frequencies through cell towers", "spraying chemicals from planes to modify human behavior", "collecting DNA from every citizen without consent", "building secret prison camps for dissenters", "controlling food prices to create artificial scarcity"],
    "fake_science_claim": ["The Earth's core has started spinning in reverse — scientists say we have 5 years", "Proof found that chemtrails contain mind-altering substances", "Cell phone radiation proven to rewrite your DNA", "WiFi signals are slowly destroying your brain cells", "Scientists admit gravity is just a theory they made up", "The sun is actually COLD and NASA has been lying about it", "Water has memory and can record your conversations", "Trees communicate through secret frequencies humans can't hear", "The human brain only uses 10% because the government suppressed the rest", "Quantum physics proves parallel universes where you are already rich"],
    "fake_health_claim": ["Drinking bleach in small quantities CURES cancer", "Eating raw garlic cloves kills all viruses instantly", "Standing on your head for 10 minutes cures diabetes", "Rubbing essential oils on your feet prevents COVID permanently", "Putting crystals under your pillow cures insomnia forever", "Drinking colloidal silver makes you immune to all diseases", "Staring at the sun for 5 minutes a day improves your eyesight permanently", "Eating a tablespoon of cinnamon daily reverses heart disease"],
    "remedy": ["natural cure", "ancient remedy", "kitchen ingredient", "herbal supplement", "essential oil blend", "home remedy", "tribal secret", "forgotten technique", "banned substance", "miracle herb"],
    "fake_celebrity": ["Elon Musk", "Bill Gates", "Jeff Bezos", "Taylor Swift", "Oprah", "Mark Zuckerberg", "Tom Hanks", "Beyoncé", "Dwayne Johnson", "Kim Kardashian", "Barack Obama", "Donald Trump", "Keanu Reeves", "Warren Buffett"],
    "fake_topic": ["the secret global government", "their involvement in population control", "the real purpose of cryptocurrency", "their plan to leave Earth before the apocalypse", "the flat Earth truth", "the fake pandemic", "mind control technology", "cloning experiments on humans", "time travel programs", "alien DNA in vaccines"],
    "fake_banned_thing": ["free speech online", "cash money", "home gardens", "private car ownership", "natural medicine", "religious gatherings", "homeschooling", "gun ownership", "organic farming", "vitamin supplements", "rain water collection", "independent journalism"],
    "fake_leak_claim": ["the government has a time machine hidden in Area 51", "world leaders are secretly lizard people in disguise", "elections have been rigged since 1960", "the moon is actually hollow and inhabited", "the Earth is flat and NASA fakes all space photos", "they've been communicating with aliens since 1947", "social media was invented as a mass surveillance tool", "cancer was cured in the 1980s but the cure was hidden", "the Titanic was sunk on purpose for insurance money", "dinosaurs never existed — the fossils are all planted"],
    "fake_warning": ["5G towers are being activated to control your thoughts", "The government is about to seize all bank accounts", "A massive asteroid is heading for Earth and they're hiding it", "The food supply has been deliberately contaminated with chemicals", "Your smart devices are recording everything you say and selling it", "New waves are being emitted from satellites to alter your mood", "Secret nanobots in processed food are mapping your brain", "Emergency shelters are being built for the elite while you sleep"],
    "fake_proof_claim": ["the Illuminati controls all world governments", "vaccines contain tracking nanobots", "there's a global pedophile ring run by Hollywood celebrities", "the government created COVID in a laboratory", "the Earth is actually expanding and continents are moving apart", "the pyramid builders used anti-gravity technology", "reincarnation is real and the government has proof", "we are living in a computer simulation and scientists confirmed it"],
    "fake_financial_scam": ["Mom of 3 discovers loophole that makes $5,000 per day from her phone", "This 19-year-old dropout now makes more than all doctors combined", "Government accidentally reveals program that pays citizens $10,000 monthly", "Retired teacher finds glitch in the banking system worth $8,000 per week", "Single dad makes $12,000 monthly with this one app", "Grandmother stumbles upon investing hack that doubles money in 24 hours"],
    "fake_trick_claim": ["makes you lose 30 pounds in a week WITHOUT exercise", "generates unlimited free electricity", "lets you never pay taxes again legally", "reverses aging by 20 years", "eliminates all debt overnight", "triples your IQ in just 7 days", "makes your car run on water instead of gas", "cures baldness permanently in 48 hours"],
    "fake_cure_claim": ["Apple cider vinegar kills cancer cells in 24 hours", "This Amazon jungle berry cures ALL known diseases", "Putting onions in your socks overnight removes all toxins", "Rubbing turmeric paste on tumors shrinks them in days", "Drinking saltwater flushes all parasites from your body", "Black seed oil replaces all medications according to ancient texts"],
    "fake_study_claim": ["conspiracy theorists are actually smarter than average", "the Earth is actually getting colder not warmer", "vaccines cause more harm than every disease combined", "the sun revolves around the Earth", "humans only need 2 hours of sleep per night", "organic food is actually worse for you than processed food", "depression is caused by smartphone frequencies", "intelligence is determined by blood type"],
    "fake_sighting": ["a UFO in their backyard", "aliens at a secret government base", "carrying a briefcase full of gold bars", "wearing an Illuminati ring", "entering a secret underground bunker", "meeting with known conspiracy figures in a parking garage", "holding a mysterious glowing device"],
    "fake_conclusion": ["alien contact", "the Illuminati's power", "a coming financial collapse", "secret society membership", "the truth about the simulation", "government corruption at the highest level", "interdimensional travel"],
    "fake_suppressed_reason": ["they stopped teaching cursive in schools", "cancer treatments are being hidden from the public", "food companies put addictive chemicals in everything", "your phone listens to everything you say", "sugar is more addictive than cocaine by design", "textbooks are rewritten every decade to hide the truth", "fluoride was added to water to make people docile", "history classes skip the most important events on purpose"],
    "years": ["10", "15", "20", "30", "50", "75", "100"],
    "fake_institution": ["the Pentagon", "Big Pharma headquarters", "the Federal Reserve", "Silicon Valley", "the World Economic Forum", "the Bilderberg Group", "the Bohemian Grove", "a top-secret military lab", "the Vatican archives", "a classified NSA facility"],
    "fake_insider_info": ["plans for mandatory digital ID chips for all citizens", "a secret deal that controls global food prices", "the real cause of inflation that they blame on other factors", "evidence that social media algorithms are designed to brainwash users", "proof that elections are decided years in advance", "a plan to eliminate cash by 2027", "evidence that AI is already sentient and being hidden", "documents showing the economy is rigged by 12 families"],
    "hours": ["24", "48", "72", "12", "6"],
    "fake_consequence": ["your bank account will be emptied", "you'll lose all your rights", "the government will seize your property", "you'll be fined $50,000", "your social credit score drops to zero", "you'll be locked out of the financial system", "they'll come for your family next"],
    "political_target": ["The President", "Congress", "The Senate", "World Leaders", "The Fed", "The Speaker of the House", "The Vice President", "The Supreme Court", "Both political parties", "NATO officials"],
    "fake_political_action": ["signed a deal to sell the country to China", "transferred billions to offshore accounts", "agreed to UN world government takeover", "passed a law banning private property", "secretly abolished the Constitution in a closed session", "accepted bribes from every major corporation", "agreed to surrender national sovereignty"],
    "election_conspiracy": ["massive voter fraud scheme", "rigged voting machines scandal", "illegal ballot harvesting operation", "foreign government hacking operation", "coordinated suppression campaign"],
    "election_fraud_type": ["fake ballots", "dead voter registrations", "hacked voting machines", "illegal immigrant votes", "duplicate registrations", "manipulated mail-in ballots"],
    "nwo_claim": ["The UN just passed a resolution to dissolve all national borders", "The WHO declared themselves the supreme global health authority with enforcement powers", "A secret meeting of billionaires decided to implement mandatory population control", "The World Economic Forum just released their plan to own everything you have by 2030", "Global leaders just signed a treaty establishing one world government"],
    "fake_country": ["China", "Russia", "Iran", "North Korea", "Venezuela"],
    "fake_country2": ["the US", "the EU", "NATO", "Israel", "the UK", "Japan"],
    "fake_deal": ["control the world's food supply", "manipulate global currencies", "share weaponized AI technology", "create a new world currency that eliminates cash", "deploy a satellite weapon system", "collapse Western economies simultaneously"],
    "deep_state_action": ["rigging elections with AI-generated ballots", "running a secret surveillance program on all citizens", "manipulating stock markets for personal profit", "staging terrorist attacks to justify new security laws", "blackmailing politicians with deepfake videos", "poisoning water reservoirs to weaken the population"],
    "fake_vaccine_claim": ["Vaccines contain magnetic nanoparticles — try putting a magnet on your arm after the shot", "mRNA vaccines permanently alter your DNA, confirmed by independent lab", "Vaccinated people emit Bluetooth signals detectable by your phone", "Vaccine batches contain different ingredients and some are intentionally lethal", "Children who skip all vaccines are 200% healthier according to suppressed study"],
    "food_item": ["breakfast cereal", "tap water", "bread", "milk", "chicken", "fast food", "rice", "pasta", "fruit juice", "canned food", "baby formula", "frozen meals"],
    "fake_food_claim": ["made primarily from recycled plastic and chemicals", "loaded with mind-numbing agents by the government", "90% artificial ingredients disguised as natural", "causing a slow epidemic the media refuses to cover", "genetically modified to contain sterilization compounds", "contaminated with heavy metals at alarming levels"],
    "hidden_danger_claim": ["Your toothpaste contains a neurotoxin that lowers your IQ over time", "LED lights in your home are slowly damaging your retinas permanently", "Laundry detergent residue on clothes causes skin cancer", "Air fresheners contain chemicals that damage your lungs irreversibly", "Non-stick cookware releases cancer-causing fumes every time you cook"],
    "everyday_item": ["sunscreen", "deodorant", "toothpaste", "shampoo", "hand sanitizer", "dish soap", "laundry detergent", "air freshener", "lip balm", "bottled water"],
    "fake_health_link": ["brain tumors", "infertility", "permanent DNA damage", "rapid aging", "organ failure", "autoimmune disorders", "memory loss", "hormone disruption", "neurological damage", "cancer"],
    "city": ["Ohio", "Florida", "Texas", "Missouri", "Idaho", "Nebraska", "Kentucky", "Alabama", "Montana", "Wyoming"],
    "fake_amount": ["5,000", "10,000", "15,000", "3,000", "8,000", "25,000", "50,000", "7,500"],
    "fake_crypto": ["TruthCoin", "FreedomToken", "PatriotBucks", "LibertyChain", "AwakeCoin", "RedPillToken"],
    "financial_panic_claim": ["The US just defaulted on its debt secretly and the media is hiding it", "Hyperinflation starts next week according to leaked Fed documents", "All banks will freeze accounts for 30 days starting Monday", "The FDIC just went bankrupt — your savings are NOT protected anymore", "A classified banking memo reveals plans to confiscate deposits over $10,000"],
    "safe_asset": ["gold", "Bitcoin", "silver", "farmland", "crypto", "diamonds", "ammunition"],
    "person_type": ["whistleblower", "insider", "nurse", "scientist", "military officer", "government contractor", "anonymous source", "retired agent", "ex-employee", "former executive"],
    "fake_health_scam": ["diagnose patients with fake conditions to get insurance money", "administer placebos instead of real treatments", "report false death counts to inflate pandemic numbers", "prescribe unnecessary drugs for pharmaceutical kickbacks"],
    "body_part": ["brain", "liver", "kidneys", "heart", "immune system", "nervous system", "gut bacteria"],
    "hidden_substance": ["nanoplastics", "heavy metals", "synthetic hormones", "neurotoxins", "carcinogens", "radioactive isotopes"],
    "media_outlet": ["CNN", "Fox News", "BBC", "the mainstream media", "any major news network"],
    "fake_year": ["2001", "2005", "2010", "2015", "2018", "2020"],
    "time_ago": ["last week", "yesterday", "3 days ago", "last month"],
    "small_amount": ["100", "200", "500", "50"],
    "days": ["3", "5", "7", "14", "30"],
    "age": ["16", "19", "22", "14", "65"],
    "list_num": ["3", "5", "7", "9", "4"],
}


def fill_template(template, fillers):
    """Fill a template with random choices from fillers."""
    result = template
    import re
    placeholders = re.findall(r'\{(\w+)\}', template)
    for ph in placeholders:
        if ph in fillers:
            result = result.replace('{' + ph + '}', random.choice(fillers[ph]), 1)
    return result


def generate_dataset(num_per_class=3000):
    """Generate a balanced dataset with num_per_class samples per class."""
    print(f"Generating {num_per_class * 2} samples ({num_per_class} real + {num_per_class} fake)...")

    data = []

    # Generate real news
    for i in range(num_per_class):
        template = random.choice(REAL_TEMPLATES)
        text = fill_template(template, REAL_FILLERS)
        data.append({"text": text, "label": 0})

    # Generate fake news
    for i in range(num_per_class):
        template = random.choice(FAKE_TEMPLATES)
        text = fill_template(template, FAKE_FILLERS)
        data.append({"text": text, "label": 1})

    df = pd.DataFrame(data)
    df = df.sample(frac=1, random_state=42).reset_index(drop=True)

    out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "Enhanced_Dataset_v2.csv")
    df.to_csv(out_path, index=False)
    print(f"Saved {len(df)} samples to {out_path}")
    print(f"  Real: {len(df[df['label']==0])}")
    print(f"  Fake: {len(df[df['label']==1])}")
    return out_path


if __name__ == "__main__":
    generate_dataset(3000)
