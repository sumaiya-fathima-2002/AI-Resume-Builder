# AI-Resume-Builder

The modern recruitment process is plagued by The Resume Black Hole. On one side, HR 
departments are overwhelmed by high-volume, unstructured PDF data that is often inconsistent in 
format and terminology, leading to an average of 75% of qualified resumes being ignored by 
traditional, rigid ATS filters. On the other side, job seekers submit applications into a void, receiving 
no developmental feedback or direction. 
SkillSmart AI addresses this two-sided inefficiency. The core problem is the lack of an intelligent, 
bidirectional system that can: 
 Accurately extract and normalize data from diverse PDF layouts. 
 Predict professional domains using semantic context rather than keyword frequency. 
 Quantify the distance between a candidate's current skills and market-standard job descriptions 
to provide real-time career guidance. 

**Objectives** 
To solve the aforementioned problems, this project is defined by the following technical and 
functional objectives: 
1. **Information Extraction & Normalization**: To develop a robust parser using pdfplumber 
and Regex that achieves a 95%+ accuracy rate in extracting entities (Email, Skills, Contact) 
from unstructured PDF documents. 
2. **Semantic Domain Classification**: To implement a Zero-Shot Classification pipeline using 
the BART-Large-MNLI model, allowing the system to categorize resumes into technical fields 
without the need for domain-specific training data. 
3. **Prescriptive Skill-Gap Analysis**: To engineer an algorithm that compares extracted skills 
against a master Skill-Map, generating a "Resume Strength Score" and identifying specific 
missing competencies. 
4. **Dynamic Resource Mapping**: To create a personalized user dashboard that provides context
aware learning resources (videos and advice) based on the predicted field and identified gaps. 
5. **Relational Data Persistence**: To design a MySQL-backed architecture that archives 
candidate profiles for long-term HR analytics and recruiter-side visualization. 

** Proposed Framework Overview **
The framework operates as a Reactive SaaS (Software-as-a-Service) platform. It is built entirely 
within the Python ecosystem, leveraging the synergy between specialized libraries for different tasks. 
 **The Presentation Layer** is built on Streamlit, transforming Python scripts into a dynamic 
web interface that reacts instantly to user inputs (uploads, button clicks). 
 **The Intelligence Layer** bypasses traditional model training by integrating Hugging Face 
Transformers. It utilizes a pre-trained BART model for Zero-Shot Classification, allowing 
for immediate deployment ("cold start") without needing a labeled dataset. 
 **The Persistence Layer** relies on a relational MySQL database, ensuring that every interaction 
is logged for future analytical processing (OLAP). 
This framework addresses the "feedback vacuum" identified in the literature review by ensuring the 
data flow is bidirectional: data goes in for analysis and comes back out as actionable career advice. 
<img width="645" height="430" alt="image" src="https://github.com/user-attachments/assets/5a909805-8c1a-4c97-b054-f98dc56e01b0" />
