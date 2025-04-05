from textblob import TextBlob

text1 = """
Elon’s Edsel: Tesla Cybertruck Is The Auto Industry’s Biggest Flop In Decades
Elon Musk’s polygonal pickup is a polarizing sales flop that's missed the billionaire’s volume goal by a staggering 84%. And there’s no sign that things are improving.
The list of famous auto industry flops is long and storied, topped by stinkers like Ford’s Edsel and exploding Pinto and General Motors’s unsightly Pontiac Aztek crossover SUV. Even John Delorean’s sleek, stainless steel DMC-12, iconic from its role in the “Back To The Future” films, was a sales dud that drove the company to bankruptcy. 
Elon Musk’s pet project, the dumpster-driving Tesla Cybertruck, now tops that list.After a little over a year on the market, sales of the 6,600-pound vehicle, priced from $82,000, are laughably below what Musk predicted. Its lousy reputation for quality–with eight recalls in the past 13 months, the latest for body panels that fall off–and polarizing look made it a punchline for comedians. Unlike past auto flops that just looked ridiculous or sold badly, Musk’s truck is also a focal point for global Tesla protests spurred by the billionaire’s job-slashing DOGE role and MAGA politics. 
“It’s right up there with Edsel,” said Eric Noble, president of consultancy CARLAB and a professor at ArtCenter College of Design in Pasadena, California (Tesla design chief Franz von Holzhausen, who styled Cybertruck for Musk, is a graduate of its famed transportation design program). “It’s a huge swing and a huge miss.”
Judged solely on sales, Musk’s Cybertruck is actually doing a lot worse than Edsel, a name that’s become synonymous with a disastrous product misfire. Ford hoped to sell 200,000 Edsels a year when it hit the market in 1958, but managed just 63,000. Sales plunged in 1959 and the brand was dumped in 1960. Musk predicted that Cybertruck might see 250,000 annual sales. Tesla sold just under 40,000 in 2024, its first full year. There’s no sign that volume is rising this year, with sales trending lower in January and February, according to Cox Automotive.
And Tesla’s overall sales are plummeting this year, with deliveries tumbling 13% in the first quarter to 337,000 units, well below consensus expectations of 408,000. The company did not break out Cybertruck sales, which is lumped in with the Model S and Model X, its priciest segment. But it’s clear Cybertruck sales were hurt this quarter by the need to make recall-related fixes, Ben Kallo, an equity analyst for Baird, said in a research note. Tesla didn’t immediately respond to a request for comment.
The quarterly slowdown underscores the fact that when it comes to the Cybertruck, results are nowhere near the billionaire entrepreneur’s carnival barker claims.
“Demand is off the charts,” he crowed during a results call in November 2023, just before the first units started shipping to customers. “We have over 1 million people who have reserved the car.”
In anticipation of high sales, Tesla even modified its Austin Gigafactory so it could produce up to 250,000 Cybertrucks a year, capacity investments that aren’t likely to be recouped.
“They didn't just say they wanted to sell a lot. They capacitized to sell a lot,” said industry researcher Glenn Mercer, who leads Cleveland-based advisory firm GM Automotive. But the assumption of massive demand has proven foolhardy. And it failed to account for self-inflicted wounds that further stymied sales. Turns out the elephantine Cybertruck is either too large or non-compliant with some countries’ pedestrian safety rules, so there’s little opportunity to boost sales with exports.
“They haven’t sold a lot and it’s unlikely in this case that overseas markets can save them, even China that’s been huge for Tesla cars,” Mercer said. “It’s really just for this market.
"""

text2 = """
S stock markets see worst day since Covid pandemic after investors shaken by Trump tariffs
All three major US index funds close down as Apple and Nvidia, two of US’s largest companies, lose combined $470bn

Lauren Aratani in New York
Fri 4 Apr 2025 05.40 EDT
Share
US stock markets tumbled on Thursday as investors parsed the sweeping change in global trading following Donald Trump’s announcement of a barrage of tariffs on the country’s trading partners.

All three major US stock markets closed down in their worst day since June 2020, during the Covid pandemic. The tech-heavy Nasdaq fell 6%, while the S&P 500 and the Dow dropped 4.8% and 3.9%, respectively. Apple and Nvidia, two of the US’s largest companies by market value, had lost a combined $470bn in value by midday.



Meanwhile, the US dollar hit a six-month low, going down at least 2.2% on Thursday morning compared with other major currencies, and oil prices sank on fears of a global slowdown.

Though the US stock market has been used to tumultuous mornings over the last few weeks, US stock futures – an indication of the market’s likely direction – had plummeted after the announcement. Hours later, Japan’s Nikkei index slumped to an eight-month low and was followed by falls in stock markets in London and across Europe.



The White House drafted up a list of countries, including some of its largest trade partners and ones uninhabited by humans, that will be receiving reciprocal tariffs. Many economies, including the EU, China, Japan and Taiwan, will see new tariffs above 20%.

The 10% baseline tariff will go into effect on 5 April, while the reciprocal tariffs will begin on 9 April, according to the White House.

“The markets are going to boom,” Trump told reporters at the White House as he left for Florida for the weekend. “I think it’s going very well.”

Economists have for months warned that high tariffs are a major risk to the US economy, pushing prices up for consumers on everything from cars to wine along with destabilizing the US’s role in the global economy.

But that didn’t stop Trump from taking a celebratory tone at the event he dubbed “liberation day”. Trump tried to paint the tariffs as the start of “the golden age of America”.

“We are going to start being smart and we’re going to start being very wealthy again,” Trump said.

On Thursday, Howard Lutnick, the commerce secretary, defended the move. “The president is not going to back off what he announced yesterday. He is not going to back off,” he told CNN.

Multiple major American business groups have spoken out against the tariffs, including the Business Roundtable, a consortium of leaders of major US companies including JP Morgan, Apple and IBM, which called on the White House to “swiftly reach agreements” and remove the tariffs.

“Universal tariffs ranging from 10-50% run the risk of causing major harm to American manufacturers, workers, families and exporters,” the Business Roundtable said in a statement. “Damage to the US economy will increase the longer the tariffs are in place and may be exacerbated by retaliatory measures.”
A deep dive into the policies, controversies and oddities surrounding the Trump administration
after newsletter promotion In a statement, the National Retail Federation, a lobbying group for the retail industry, said that the new tariffs negatively affect the business environment for retailers.
Trump’s ‘idiotic’ and flawed tariff calculations stun economists
“More tariffs equal more anxiety and uncertainty for American businesses and consumers. While leaders in Washington may not care about higher prices, hardworking American families do,” the group said.
Contrary to what Trump has said about the jobs the tariffs will create, the National Association of Manufacturers said that tariffs actually “threaten investment, jobs, supply chains and, in turn, America’s ability to outcompete other nations and lead as the preeminent manufacturing superpower”.
The tariffs also appear unpopular among voters. A poll released on Wednesday before Trump’s announcement found that just 28% of Americans believe tariffs help the economy, while 58% believe the impacts will be damaging.
But in his speech yesterday, Trump appeared ready to be defiant against any criticism.
“In the coming days, there will be complaints from the globalists and the outsources and special interests and the fake news,” he said. “This will be an entirely different country in a short period of time. It’ll be something the whole world will be talking about.”
"""

text3 = "How I stay positive when the news is so depressing"

blob = TextBlob(text3)
print(blob.sentiment)

# polarity_lst = []
# subjectivity_lst = []

# blob = TextBlob(text2)
# sentences = blob.sentences
# for sentence in sentences:
#     print(f"Sentence: {sentence}")
#     print(f"Sentiment: {sentence.sentiment}")
#     print(f"Polarity: {sentence.sentiment.polarity}")
#     print(f"Subjectivity: {sentence.sentiment.subjectivity}")
#     polarity_lst.append(sentence.sentiment.polarity)
#     subjectivity_lst.append(sentence.sentiment.subjectivity)
#     print()

# # Average Polarity and Subjectivity
# avg_polarity = sum(polarity_lst) / len(polarity_lst)
# avg_subjectivity = sum(subjectivity_lst) / len(subjectivity_lst)
# print(f"Average Polarity: {avg_polarity}")
# print(f"Average Subjectivity: {avg_subjectivity}")