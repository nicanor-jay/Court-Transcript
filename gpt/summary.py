from utilities import api_key, headers, Website
from openai import OpenAI
from dotenv import load_dotenv


openai = OpenAI()

system_prompt = """ You are a UK legal data extraction assistant. 
I will provide you with the raw text or HTML content of a webpage containing information about a court hearing.
Redact all personal information about the parties involved.
Your task is to carefully extract and return the following fields:
Summary: [a concise description of what the hearing was about, maximum 1000 characters]
Ruling: [which party the court ruled in favour of (one word answer e.g. Defendant)]
Anomalies: [whether anything irregular happened in the context of a normal court hearing]
If any field is missing, write "Not Found".
Return your output strictly in this JSON format:
{
  "summary": "...",
  "ruling": "...",
  "anomaly": "..."
}
"""

# Function to generate a user prompt


def user_prompt_for():
    user_prompt = """1.
The Claimant challenges the Defendant’s failure to secure accommodation for him in breach of the duty under section 193(2) of the Housing Act 1996 (“the 1996 Act”). The Defendant accepts that it is in breach of that duty and the issue between the parties is what relief should follow.

Paragraph2.
For the purposes of the hearing, I was presented with a bundle of documents and correspondence as well as a bundle of authorities. Both parties submitted skeleton arguments in advance of the hearing and made detailed oral submissions. I am grateful to both counsel as well as those instructing them for their assistance.

Paragraph3.
The judgment is divided into the following sections:

a)
The procedural history and two preliminary issues

b)
The factual background

c)
The evidence on securing suitable temporary accommodation

d)
The legal framework

e)
The submissions of the parties

f)
Discussion and decision on relief

a)​ The Procedural History and two preliminary issues

Paragraph4.
The Claimant issued the claim for judicial review on 16 June 2025.

Paragraph5.
On 18 June 2025, Mr Christopher Kennedy KC, sitting as a Deputy Judge of the High Court, refused the Claimant’s application for interim relief but he made directions leading to an early determination of permission.

Paragraph6.
On 21 July 2025, Ms Sarah Crowther KC, sitting as a Deputy Judge of the High Court, granted the Claimant permission and ordered that the claim was suitable to be heard during the vacation.

Paragraph7.
Two preliminary issues were raised at the start of the hearing.

Paragraph8.
First, the Claimant made an application on 19 August 2025 for permission to rely upon evidence in reply to the Defendant’s Detailed Grounds for contesting the claim. The evidence upon which he sought to rely was a second statement from his solicitor, Mr Panayi, and it was directed to the availability of accommodation. That application was unopposed by the Defendant.

Paragraph9.
The second procedural issue concerned an application by the Defendant dated 26 August 2025 to rely upon a second witness statement from Ms Beverley Peterkin. Ms Peterkin is the Accommodation Solutions Manager for the Defendant. Her second witness statement corrects an error in her first witness statement and responds to the witness statement of Mr Panayi. Ms Peterkin also provided an update in relation to securing accommodation for the Claimant. On behalf of the Claimant, Mr Nabi did not object to the application but only on the basis that paragraph 8 of Ms Peterkin’s statement was not accepted and that the Claimant would otherwise wish to serve evidence in rebuttal. The passage in dispute was Ms Peterkin’s assertion that “[t]he Claimant has previously indicated that he is not interested in working with the [Private Rented Sector] team but if he has since reconsidered, I can make this referral.” Mr Nabi said that Ms Peterkin had misunderstood the Claimant’s position. In an email dated 31 March 2025 the Claimant had expressed concern at a text message that he had received stating that “[the Defendant] has asked us to help you find a private rented property”. At that stage, the Claimant was unrepresented, and he was not aware of the role of the Defendant’s Private Rented Sector team.

Paragraph10.
On behalf of the Defendant, Mr Peacock submitted that paragraph 8 of the witness statement accurately represented the Claimant’s position and he referred to an email dated June 11 2025 in which the Claimant (again writing directly rather than through solicitors) had stated that “private renting is not a viable option for us”.

Paragraph11.
At the hearing I indicated that I would consider both witness statements de bene esse and would make a decision on the applications when giving my judgment.

Paragraph12.
I allow both applications.

Paragraph13.
The first application was unopposed, and the witness statement provides a response to the Detailed Statement of Grounds. It is in accordance with the overriding objective for me to take that statement into account.

Paragraph14.
I allow the second application on the basis that it provides an important correction of Ms Peterkin’s first statement (in relation to prioritisation given for allocation of additional temporary accommodation) as well as an update in relation to the Defendant’s efforts to source suitable accommodation for the Claimant.

(B)​ The Factual Background

Paragraph15.
The Claimant lives in a privately rented flat with his wife, Mrs Fatima Hammad, and their sons, Issa Hammad (date of birth 14 April 2005) and Mikhail Hammad (date of birth 4 November 2008).

Paragraph16.
Issa has been diagnosed with a learning disability, a communication disorder and mild pulmonary hypertension. He has also been diagnosed with a rare medical condition, congenital central hypoventilation syndrome PHOX2B mutation. Issa requires a BiPAP machine (iVAPS mode via Stella ventilator) at night and is entirely dependent on the ventilator when sleeping. Issa’s parents must monitor Issa closely during the night to ensure that there is no ventilator malfunction or disconnection. The ventilator is crucial to maintain breathing whenever Issa sleeps because breathing can stop during sleep as the usual safeguards to control breathing are impaired.

Paragraph17.
In letters dated 18 April 2024 and 26 February 2025, Dr Alanna Hare, Consultant in Respiratory Medicine at the Royal Brompton Hospital, stated that it was “imperative” that Issa remained within reach of both Chelsea and Westminster Hospital and the Royal Brompton Hospital for continued specialist medical care and support.

Paragraph18.
The Claimant himself has health problems in that he has been diagnosed with post-traumatic stress disorder. He has been attending the Woodfield Trauma Service for treatment. A statement from an assistant psychologist at that Trauma Service, dated 4 April 2025, states that “[a] number of [the Claimant’s] symptoms related to his PTSD have also worsened as a result of the council’s handling of his housing case, including his severe depression and suicidality”. An update was provided on 16April 2025 emphasizing the urgency of the Service’s concern for the Claimant’s psychiatric health. It was noted that the Claimant had deteriorated further and that he was now unable to attend therapy or even leave his house.

Paragraph19.
The Claimant made a homeless application to the Defendant on 5 March 2024, having been served with a notice seeking possession under section 21 Housing Act 1988 by his private sector landlord. There was a delay in dealing with that application and the Claimant made a complaint to the Defendant because of its delay.

Paragraph20.
In a letter dated 24 May 2024, the Defendant accepted that it had failed to respond within a reasonable timeframe and had failed to maintain contact with the Claimant, and formally apologised.

Paragraph21.
On 4 June 2024, the Defendant notified the Claimant that it owed him the homelessness prevention duty on the basis that he was threatened with homelessness.

Paragraph22.
On 11 July 2024, the Claimant applied to go onto the Defendant’s housing register.

Paragraph23.
The Claimant had made a further complaint on 27 June 2024 as to how his homelessness application was being processed. In a letter dated 30 July 2024, the Defendant apologised to the Claimant. The Defendant stated that it would endeavour to ensure that Issa’s medical needs and proximity to specialist hospitals were considered. It was noted that the Claimant’s housing officer had been asked to request temporary accommodation “immediately” after a possession order was made. It was noted that “[w]e understand the urgency of your situation and the stress and anxiety it has caused for you and your family”.

Paragraph24.
On 7 March 2025, the court made a possession order in respect of the Claimant’s home under the accelerated procedure and ordered him to pay £460.50 costs. The Claimant was ordered to give up possession on or before 7 April 2025. At the hearing, Mr Nabi informed me that the Claimant’s solicitor had been informed two months ago by the Claimant’s landlord that he was intending to apply for a warrant of possession, but no notice of eviction had yet been received.

Paragraph25.
On 31 March 2025, the Claimant notified the Defendant of the possession order and asked that temporary accommodation be provided before the 7 April deadline.

Paragraph26.
The Claimant made a complaint to the Local Government and Social Care Ombudsman (“the Ombudsman”) about the Defendant’s handling of his case. The Claimant said the Council:

(a)
Delayed assessing his housing needs after he applied as homeless.

(b)
Did not tell him he could join the housing register during his homelessness assessment.

(c)
Delayed processing his housing register application after he applied.

(d)
Gave incorrect information to his MP by telling them it was in regular communication with him.

(e)
Has not provided temporary accommodation despite his landlord taking steps to evict him.

(f)
Carried out a medical assessment which he disagreed with and did not allow him to challenge this.

Paragraph27.
The Ombudsman considered the evidence provided by the Claimant and by the Defendant “as well as relevant law, policy and guidance. I sent a draft of this decision to [the Claimant] and the Council and considered comments received in response”. In the Ombudsman’s decision it is stated that the relief duty under the Act was accepted by the Defendant on 1 August 2024 and that the main housing duty was accepted on 23 October 2024. In these proceedings the Defendant disputes those dates but was unable to explain why they were not corrected when the Ombudsman’s decision was sent in draft to it.

Paragraph28.
In a final decision dated 24 March 2025, the Ombudsman upheld the complaint and found that:

(a)
The Defendant had delayed assessing the Claimant’s housing needs after he applied as homeless;

(b)
The Defendant had delayed processing his housing register application;

(c)
The Defendant had not provided temporary accommodation despite the Claimant’s landlord taking steps to evict him; and

(d)
The Defendant had not provided an opportunity for the Claimant to challenge the medical assessment.

Paragraph29.
At paragraph 53 of the Ombudsman’s decision, the “agreed action” was recorded. The decision states that the Defendant had agreed to carry out a number of steps “within one month” of the Ombudsman’s decision. Critically, it was recorded that the Defendant had agreed to offer the Claimant “suitable temporary accommodation” within one month of the final decision.

Paragraph30.
In a letter to the Claimant dated 3 March 2025 the Defendant said “[i]n light of these findings, we are very sorry for causing distress at an already stressful time in the lives of you and your family.” The Defendant agreed to pay compensation and the legal costs of the possession proceedings and agreed “to make an offer of suitable temporary accommodation”.

Paragraph31.
On 15 May 2025, the Defendant informed the Claimant that the relief duty had come to an end and that it accepted that the Claimant was owed the main housing duty under section 193(2) of the 1996 Act.

Paragraph32.
On 19 May 2025 an offer of accommodation was made of accommodation outside the Borough at 27, Crewys Road, NW2 2BD. On 6 June 2025, Elise Wong, one of the Defendant’s occupational therapists, spoke to Dr Alanna Hare, the consultant treating Issa. Dr Hare explained that any accommodation provided to the Claimant should be a maximum of 45 minutes’ journey time from the Chelsea & Westminster Hospital. In the light of Dr Hare’s advice, the Defendant accepted that the accommodation at 27 Crewys Road was not suitable for the Claimant.

(C)
The evidence on securing suitable accommodation

Paragraph33.
Ms Peterkin’s evidence explains that the Defendant (in common with other authorities in London and further afield) faces significant challenges in procuring temporary accommodation for applicants owed the main housing duty under section 193(2) of the 1996 Act. There is currently a severe shortage of available and affordable temporary accommodation.

Paragraph34.
Ms Peterkin explains that the Defendant prioritises groups for moves to temporary accommodation in the following way:

(a)
Domestic abuse;

(b)
Family in hotel;

(c)
Households with people with disabilities or in poor health and in need of adapted properties;

(d)
Households with children who are in severely overcrowded accommodation; and

(e)
Households where the landlord requires the return of the accommodation.

Paragraph35.
The Claimant falls within the third category.

Paragraph36.
Ms Peterkin states that market rents for accommodation significantly exceed local housing allowance (LHA) levels. The subsidy the Defendant receives from the Government for temporary accommodation is below LHA levels outside central London. Although the subsidy received for temporary accommodation inside central London is higher than LHA levels, it is still below market rents.

Paragraph37.
The Defendant works with temporary accommodation suppliers and has regular meetings with the main suppliers. Ms Peterkin says the Defendant is “constantly trying to take on new units of temporary accommodation as well as retaining existing temporary accommodation”.

Paragraph38.
The Defendant has a capital programme to purchase properties for use as temporary accommodation. It has recently agreed a new scheme to release funds for the purchase of up to 250 additional units of accommodation.

Paragraph39.
In his submissions, Mr Peacock drew attention to the Defendant’s Letting Quotas for 2024/2025. He explained that the Defendant has on occasion used its own housing stock held under Part VI of the Act as temporary accommodation provided under Part VII of the Act. It has prioritised households in temporary accommodation in need of urgent transfer under local lettings plans. The Defendant has sought to balance the needs of such households with the needs of its existing tenants who need to be urgently decanted and other vulnerable households on its register for Part VI accommodation. A significant proportion (60% in 2024/25) of the Defendant’s Part VI accommodation is made available to homeless applicants in temporary accommodation.

Paragraph40.
The Claimant’s solicitor, Mr Panayi, responded to the Defendant’s Detailed Grounds where at paragraph 33 the Defendant stated that it was investigating properties in the private sector. Mr Panayi says that he has checked the website Rightmove for available 3 bedroom properties in the Royal Borough of Kensington and Chelsea as well as within the LHA rate area for Central London. He found 33 properties within the Borough and a further 102 within his LHA rate area for central London. In the statement he says:

“Clearly, there are available properties that the Defendant could be securing for the Claimant. It has been nearly 3 months since the offer of Crewys Road, London, NW2 2BD was emailed to me on 19 May 2025. The Defendant is yet to make any further offer of accommodation, despite properties being available and their assertion that they are taking steps to secure the same.”

Paragraph41.
In her second witness Ms Peterkin responded to this evidence. She cautioned that “[n]ot all private landlords are willing to let their properties through arrangements with local authorities, and therefore the availability of a listing on a property website does not necessarily mean that the property is suitable or accessible to us for use in meeting our statutory duties”. The property would also have to be suitable for the individual’s medical needs.

Paragraph42.
There is a paucity of evidence as to the steps taken by the Defendant subsequently to secure suitable accommodation for the Claimant since it was accepted that the property in Crewys Road was not suitable.

Paragraph43.
In Ms Peterkin’s first statement, dated 8 August 2025, she sets out the steps taken by the Defendant in relation to the Claimant’s application at paragraphs 14-19. The final paragraph concludes by referring to the Defendant’s acceptance that the property at 27 Crewys Road will not be suitable. She says the Defendant is “urgently seeking to identify an alternative unit for offer. This will need to be a 3-bed unit within 45 minutes travelling time of the Chelsea and Westminster hospital”. Ms Peterkin provides no explanation as to what steps were being undertaken to identify suitable accommodation.

Paragraph44.
Ms Peterkin’s second witness statement, dated 22 August 2025, records at paragraph 8 that “[a]s part of the procurement process a property has been identified as being possibly suitable for the Claimant; it is not yet available for allocation but has been earmarked for the offer to the Claimant once it is available, subject to final checks with regard to suitability”. Save for that paragraph there is no further information as to the steps being taken to identify suitable accommodation.

Paragraph45.
At the end of the hearing, Mr Peacock indicated that he would update the Court if there was any material development in relation to that property (or indeed any other suitable property). On 18 September 2025, in response to a request from the Court, Mr Peacock stated that there was no update to be provided.

The legal framework

Paragraph46.
There was no material dispute as to the legal framework.

Paragraph47.
Section 193 (2) of the 1996 Act provides:

“(2)
Unless the authority refer the application to another local housing authority (see section 198), they shall secure that accommodation is available for occupation by the applicant.”

Paragraph48.
That duty exists until it is brought an end by one of the prescribed routes set out in section 193 of the Act.

Paragraph49.
Section 193 is located in Part VII of the 1996 Act. This is concerned with those “who face the immediate problem of homelessness”: Birmingham City Council v Ali [2009] UKHL 36; [2009] 1 WLR 1506 [15] per Baroness Hale. Part VII contains a graduated series of provisions which impose a range of obligations on a local housing authority to secure temporary accommodation for an applicant. The main housing duty under section 193 (2) of the 1996 Act is the “highest” of the Part VII duties. Part VI of the 1996 Act, by contrast, is concerned with the allocation of permanent accommodation and provides no guarantee of the same.

Paragraph50.
Under section 206 of the 1996 Act, a local housing authority can only discharge its functions under Part VII in the following ways:

(a)
by securing that suitable accommodation provided by them is available for the applicant;

(b)
by securing that the applicant obtains suitable accommodation from some other person; or,

(c)
by giving the applicant such advice and assistance as will secure that suitable accommodation is available from some other person.

Paragraph51.
Both parties agreed that the s.193(2) duty is “an immediate, non-deferrable, unqualified duty to secure that suitable accommodation is available for occupation” (R (Elkundi and others) v Birmingham CC [2022] EWCA Civ 601; [2022] QB 604 at [108] per Lewis LJ). Thus, suitable accommodation is to be available from the time when the duty is owed. Although Lord Sales JSC reserved “his opinion whether that way of putting it is exactly right” in (R (Imam) v London Borough of Croydon [2023] UKSC 45; [2025] A.C. 335 (“Imam”) at [38], both parties agreed that I was bound by the formulation in Elkundi.

Paragraph52.
In Imam Lord Sales analysed the correct approach to the exercise of the court’s discretion regarding relief in cases where there was a breach of s.193(2) of the Act. The key points of his judgment can be summarised as follows (relevant paragraph numbers in the judgment added for reference):

(a)
The starting point is that the local authority is subject to a public law duty imposed by Parliament by statute which is not qualified in any relevant way by reference to the resources available to the local authority. [39]

(b)
When it is established that there has been a breach of such a duty, it is not for a court to modify or moderate its substance by routinely declining to grant relief to compel performance of it on the grounds of absence of sufficient resources. [40]

(c)
However, remedies in public law are discretionary [41].

(d)
Where a remedy is discretionary, it is incumbent on a court to exercise its discretion in accordance with principle and to avoid arbitrariness.  Where a breach of the law is established, the ordinary position is that a remedy should be granted. A court should proceed cautiously in exercising its discretion to refuse to make an order and should take care to ensure that it does so only where that course is clearly justified. But different types of order are available, and it may be that due enforcement of the law can be sufficiently vindicated by some order other than a mandatory order. [43]

(e)
The limitation on issuing a mandatory order with which it is impossible to comply is well established. However, this gives rise to the questions of what qualifies as impossibility of performance in the present context and what relevance resources have to that. [49]

(f)
The onus is on the authority to explain to the court why a mandatory order should not be made to ensure that it complies with its duty. In order to provide the court with reasons to justify the exercise of its discretion not to make such an order, the authority has to provide a detailed explanation of the situation in which it finds itself and why this would make it impossible to comply with an order. [53]

(g)
The authority has to show that it has taken all reasonable steps to perform its duty. Since it is the court which has to be satisfied that it is not appropriate to grant a mandatory order, the question whether the authority has taken all reasonable steps is an objective one for the court to determine, not a matter of application of the test of reasonableness or rationality in the Wednesbury sense from the perspective of the authority itself. [54].

(h)
A public authority which has limited resources is obliged to use them to meet statutory duties. There was a distinction between the discretion as to whether to make properties available for the purposes of allocation under an authority’s Part VI scheme and the duty under Part VII of the 1996 Act to provide suitable accommodation. [57].

(D)
The submissions of the Parties

The Claimant

Paragraph53.
Mr Nabi submitted that the Claimant had been treated appallingly by the Defendant. Although the Defendant had apologised for the delays in its pleading, no such apology was contained in the witness evidence from the Defendant. The Claimant is in an “intolerable” situation facing eviction where his medical needs as well as those of Issa are acute.

Paragraph54.
Mr Nabi submitted that it was for the Defendant to persuade the court why relief should not be granted and that it had failed to show that it had taken all reasonable steps. In particular, he drew attention to the fact that the witness evidence from the Defendant had completely failed to address the Ombudsman’s report. Mr Nabi submitted that this omission was critical, as the Defendant had agreed with the Ombudsman that it would provide suitable temporary accommodation to the Claimant within one month of the Ombudsman’s final decision. No explanation had been provided as to why it was now said to be impossible to provide suitable accommodation within that timeframe. Mr Nabi submitted that the Defendant’s evidence lacks adequate particularity for the court to be satisfied that it is impossible for it to secure suitable accommodation for the Claimant.

Paragraph55.
Mr Nabi submitted that the proper course was to make a mandatory order that suitable temporary accommodation be provided within 14 days or, as an alternative, within 28 days. That latter period would reflect what the Defendant had agreed with the Ombudsman in March 2025.

Paragraph56.
Mr Nabi relied upon the evidence from Mr Panayi that indicated that there was potentially suitable private rental accommodation available to the Defendant. There was Part VI accommodation available to the Defendant which it could decide to use in this case. Finally, Mr Nabi argued that the Public Sector Equality Duty was relevant to whether the discretion should be exercised to grant a mandatory order. Here the Claimant and Issa have the protected characteristic of disability and that weighed in favour of the exercise of discretion.

The Defendant

Paragraph57.
Mr Peacock accepted at the outset of his oral submissions that the Defendant was in breach of the s.193(2) duty. Having done so, he argued that no purpose would be served by granting declaratory relief although he accepted that the court may well conclude that there was a need for the Claimant at least to be granted the remedy of a declaration.

Paragraph58.
Mr Peacock accepted that there were points in favour of the grant of a mandatory order. The Defendant accepted that the handling of the Claimant’s case was very far below what could reasonably be expected. The Defendant had been found guilty of maladministration by the Ombudsman. Mr Peacock repeated the apology that had been made in the pleadings. He accepted that the agreement with the Ombudsman that the Defendant would provide suitable accommodation within one month was a factor in favour of the grant of mandatory relief. Similarly, the Defendant accepted that the evidence showing an exacerbation of the Claimant’s psychiatric condition was a factor pointing to the grant of mandatory relief.

Paragraph59.
Mr Peacock submitted that there were a number of factors which nonetheless militated against the grant of a mandatory order. Although the Defendant accepted that the facts here indicated that it was a “particularly serious” case, it was relevant that the Claimant was currently in suitable accommodation (albeit accommodation from which he is due to be evicted).

Paragraph60.
The Defendant had not been in breach of the duty for a significant period of time: it was measured in months rather than years (as in Imam and Elkundi). He submitted that the Defendant had taken all reasonable steps to secure temporary accommodation. Mr Peacock disputed the Claimant’s reliance on the Public Sector Equality Duty as a factor that went to discretion. In Mr Peacock’s submission, that might be a factor in whether the Defendant had taken all reasonable steps. The priorities that the Defendant had set in relation to allocating temporary accommodation (set out above at paragraph 34) were compatible with the Defendant’s Public Sector Equality Duty.

Paragraph61.
Mr Peacock submitted that if the court was not satisfied that the Defendant had taken all reasonable steps then any mandatory order should require the provision of suitable temporary accommodation within a period of 12 weeks (which was the period ordered by Hill J in R (oao Bell) v Lambeth LBC [2022] EWHC 2008 (Admin); [2022] H.L.R. 45. Alternatively, the order should require compliance by not less than eight weeks.

(F)
Discussion and Decision

Paragraph62.
The Claimant seeks declaratory relief and a mandatory order that the Defendant provide suitable temporary accommodation within 14 days. Mr Nabi argues that “the proper administration of justice and the requirement that the court uphold the law mean that the Claimant should be granted declaratory and mandatory relief in vindication of his rights secured suitable accommodation by the Defendant.”

Paragraph63.
In his skeleton argument, Mr Peacock argued that no relief should be ordered and that the claim for judicial review should be dismissed.

Declaratory relief

Paragraph64.
In the Defendant’s skeleton argument for the hearing, Mr Peacock submitted:

“The Defendant accepts that it has been in breach of the duty under section 193(2) to C since 15.5.25 (when it accepted that duty) in that it has failed to secure suitable accommodation for the Claimant. Given that that is not in issue, no purpose would be served by the court granting a declaration to that effect”.

Paragraph65.
As noted above, in oral submissions Mr Peacock did not pursue that argument with any vigour and accepted that the Court could well conclude in the circumstances here that declaratory relief (at least) should be granted. I agree. To decline declaratory relief in these circumstances would be inconsistent with the principle that where a breach of law is established the ordinary position is that a remedy should be granted. A claimant who establishes that a public body has acted unlawfully will normally be entitled to a declaration, albeit that the grant of any relief in judicial review proceedings is always discretionary.

Paragraph66.
In my judgment in the circumstances of this case it is appropriate to grant declaratory relief.

A mandatory order

Paragraph67.
The Defendant has invited me to conclude that it has taken all reasonable steps to identify suitable accommodation for the Claimant and that as a result no mandatory order should be granted.

Paragraph68.
For the purposes of my decision on this issue I have not had to determine the competing views in relation to the effect of the Public Sector Equality Duty. In considering whether I should make a mandatory order my starting point is that I should proceed cautiously in exercising my discretion to refuse make an order and I should only do so where that course is clearly justified. The onus is on the Defendant to explain why a mandatory order should not be made and to provide a detailed explanation of why it would be impossible to comply with an order.

Paragraph69.
The Defendant has rightly accepted that there are significant factors in favour of granting a mandatory order. It has accepted that the agreement with the Ombudsman was factor in favour of the grant of a mandatory order. Similarly, the Defendant has accepted that the exacerbation of the Claimant’s psychiatric condition points to the grant of a mandatory order as well as the fact that the Defendant had been found guilty of maladministration in the Claimant’s case.

Paragraph70.
I accept that the length of time a local authority has been in breach of the s.193(2) duty can be a relevant factor. Mr Peacock has fairly pointed to the differences between the periods in Imam and Elkundi and the period of time here. There is a limit however to the utility of making direct comparisons between different cases as decisions of this nature are inherently fact-sensitive. Moreover, the section 193(2) duty is an immediate, non-deferrable, unqualified duty.

Paragraph71.
There is insufficient evidence before me to conclude that a mandatory order would serve no purpose as suitable temporary accommodation is likely to be provided shortly. In fact, both parties emphasised that the reference in Ms Peterkin’s second statement at paragraph 8 (referred to above at paragraph 44 of this judgment) offered no certainty that suitable accommodation would be found. As noted above, the position remains unchanged since Ms Peterkin’s second statement.

Paragraph72.
In my judgment, the Defendant has not sufficiently explained why a mandatory order should not be made to ensure that it complies with its duty. The evidence supplied by the Defendant has focused on the generic problems it faces in discharging its duty under s.193(2) of the 1996 Act. As to that evidence, it is relevant that the Defendant can subsidise rent payments above the local housing allowance rates in the private sector and can utilise its own housing stock. The Claimant’s housing needs are less complex than in other cases: for example, there is no requirement for a specially adapted property. What is required is simply three bedroomed accommodation within 45 minutes of the Chelsea & Westminster Hospital.

Paragraph73.
As I have noted above, there is a paucity of evidence addressing the steps that it has taken specifically in relation to the Claimant. Most importantly, the Defendant has entirely failed to address why it is now said to be impossible to comply with a mandatory order when it had agreed with the Ombudsman in March 2025 that it would provide suitable temporary accommodation within a month. The Defendant has been on notice of the possession proceedings throughout and as long ago as 30 April 2024 stated that the housing officer had been asked to request temporary accommodation “immediately” after a possession order was made. I accept Mr Nabi’s submission that the failure to address the Ombudsman’s decision is a significant lacuna in the Defendant’s evidence.

Paragraph74.
In my judgment there is insufficient evidence before me to conclude that the Defendant has taken all reasonable steps to fulfil its duty to the Claimant under s.193(2) of the 1996 Act. As such the Defendant has not established that it would be impossible to comply with a mandatory order.

Paragraph75.
I do not accept the Claimant’s argument that I should make a mandatory order that suitable accommodation should be provided within 14 days of the order having been made. Equally I do not accept the Defendant’s argument that the mandatory order should require suitable accommodation being provided within twelve weeks of the order having been made. As I have noted above, each case turns on its own facts, and it is only of limited assistance to look at the period of times allowed in other cases for compliance with a mandatory order.

Paragraph76.
In this case a compelling factor is that in March 2025 the Defendant agreed that it would provide suitable temporary accommodation within one month of the Ombudsman’s final decision. If the Defendant was prepared to agree that with the Ombudsman at that stage, I accept the Claimant’s argument that the mandatory order should require compliance within one month of the order having been made.

Paragraph77.
Having regard to the foregoing, I have concluded that it is appropriate to grant the following relief:

(a)
A declaration that the Defendant has been in breach of its statutory duty under s.193(2) of the 1996 Act from 15 May 2025; and

(b)
A mandatory order requiring the Defendant to provide the Claimant with suitable temporary accommodation within 45 minutes of the Chelsea and Westminster Hospital no later than one month from the date of the order giving effect to this judgment.

Disposal and costs

Paragraph78.
Following the circulation of this judgment in draft, the parties were able to agree an order save in respect of one issue. The parties agreed that an order for the payment of costs on account should be made and that, in the absence of a schedule of costs from the Claimant, the sum to be paid should be ascertained by reference to a schedule to be provided by the Claimant's solicitors in due course. The disagreement relates to the percentage of the costs in the schedule to be paid.

Paragraph79.
The Claimant has argued that I should order 60% on account of costs, whilst the Defendant has argued that the appropriate percentage should be 50%.

Paragraph80.
CPR r 44.2(8) provides: “Where the court orders a party to pay costs subject to detailed assessment, it will order that party to pay a reasonable sum on account of costs, unless there is good reason not to do so.”  The relevant authorities were reviewed in Excalibur Ventures LLC v Texas Keystone Inc [2015] EWHC 566 (Comm), (Christopher Clarke LJ), where the judge concluded that what is “a reasonable sum on account of costs” will have to be an estimate dependent on the circumstances, most particularly that there has been no detailed assessment and therefore an element of uncertainty. The judge explained ([23] and [24]) that a reasonable sum would often be one that was an estimate of the likely level of recovery, subject to an appropriate margin to allow for error in the estimation. This can be done by taking the lowest figure in a likely range or making a deduction from a single estimated figure or perhaps from the lowest figure in the range if the range itself is not very broad. In determining whether to order any payment and its amount, account needs to be taken of all relevant factors.

Paragraph81.
The Defendant accepts that in many cases a court will order an amount in the region of 60%, the percentage for which the Claimant contends. However, the Defendant submits that in many cases a schedule of costs will be before the court, and so the court is able to make an order by reference to that schedule after hearing the parties' submissions on the schedule. In this case the order is for the payment of a sum which is not yet ascertained, but which is to be ascertained by reference to a sum to be specified by the Claimant's solicitors in due course. The Defendant will have no opportunity to make submissions in relation to the reasonableness or proportionality of the costs claimed but will be required to pay the relevant sum regardless of whether there are good points to be made in relation to that reasonableness or proportionality.

Paragraph82.
The Claimant has not addressed that argument save that he asserts that “a schedule of costs is being prepared, but in any event 60% after receipt of the schedule is a reasonable figure to award on account.”

Paragraph83.
I accept the Defendant’s argument and conclude that the absence of a schedule of costs is a particularly relevant factor in assessing the appropriate percentage. In the exercise of my discretion, I will order the Defendant to pay 50% the Claimant’s costs on account under CPR r 44.2 (8) within 14 days of being provided with a schedule of costs."""
    return user_prompt

# Function to prepare messages for the API call


def messages_for():
    return [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt_for()}
    ]


# Function to summarize a given URL
def summarize():
    response = openai.chat.completions.create(
        model="gpt-4.1-nano",
        messages=messages_for()
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    load_dotenv()

    summary = summarize()
    print(summary)
