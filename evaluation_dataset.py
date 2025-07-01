# evaluation_dataset.py

def get_evaluation_dataset():
    """
    Returns a list of dictionaries, where each dictionary contains a question
    and the "ground truth" answer based on the content from ask.herts.ac.uk.
    """
    return [
        {
            "question": "How much does it cost to replace a lost or damaged student ID card?",
            "ground_truth": "The fee for a replacement ID card is £15."
        },
        {
            "question": "What should I do if my ID card is stolen?",
            "ground_truth": "If your ID card is stolen, you should report it to the police to get a crime reference number. The university may waive the replacement fee if you provide this number."
        },
        {
            "question": "Can I get a temporary ID slip for my exams?",
            "ground_truth": "Yes, you can obtain a temporary ID slip for exams from the Ask Herts Helpdesk if you have lost your card."
        },
        {
            "question": "What is the current application fee for a Student Visa from outside the UK?",
            "ground_truth": "The application fee for a Student Visa made from outside the UK is £490."
        },
        {
            "question": "How much is the accommodation deposit?",
            "ground_truth": "The accommodation deposit is £400, which serves as an advance payment of rent."
        },
        {
            "question": "Under what circumstances can I get a refund on my accommodation deposit?",
            "ground_truth": "A refund of the accommodation deposit is possible under specific circumstances, such as being a 'no show', visa refusal, or if the University cannot offer you accommodation."
        },
        {
            "question": "How can I prove my student status to get a council tax exemption?",
            "ground_truth": "You can request a Council Tax Exemption letter through your Student Record on the university's website."
        },
        {
            "question": "Is it possible to change my allocated accommodation room?",
            "ground_truth": "Yes, you can apply to change your accommodation, but this is subject to availability and specific application periods."
        },
        {
            "question": "I am unhappy in my accommodation, what should I do?",
            "ground_truth": "If you are unhappy in your accommodation, you should first speak to your Resident Assistant or the Accommodation Team to discuss the issues."
        },
        {
            "question": "Are there laundry facilities on campus?",
            "ground_truth": "Yes, laundry facilities are available on both the College Lane and de Havilland campuses."
        },
        {
            "question": "How do I get started with the Careers and Employment service?",
            "ground_truth": "You can get started with the Careers and Employment service by visiting their drop-in service, booking an appointment, or attending their workshops and events."
        },
        {
            "question": "What is the Post-Study Work visa?",
            "ground_truth": "The Post-Study Work visa, also known as the Graduate Route, allows eligible international students to stay in the UK to work for two years (or three for PhD graduates) after completing their course."
        },
        {
            "question": "Can I work during my studies on a Student visa?",
            "ground_truth": "Yes, students on a Student visa are usually permitted to work, but there are restrictions on the number of hours per week during term-time."
        },
        {
            "question": "What are the rules for working during my vacation period as an international student?",
            "ground_truth": "During official vacation periods, international students on a Student visa may be able to work full-time."
        },
        {
            "question": "What happens if my attendance drops as an international student?",
            "ground_truth": "Poor attendance for international students can have serious consequences, including being reported to the Home Office, which could lead to visa cancellation."
        },
        {
            "question": "What should I do if I am absent from my studies?",
            "ground_truth": "If you are absent from your studies, you must inform the University by completing the 'Notification of Absence' form online."
        },
        {
            "question": "Where can I find information about student safety and crime prevention?",
            "ground_truth": "The University provides guidance on student safety and crime prevention, which covers topics like personal safety, protecting your property, and online safety."
        },
        {
            "question": "Do I need a TV Licence to watch live TV in my student accommodation?",
            "ground_truth": "Yes, you need a TV Licence to watch or record live TV programmes on any channel, or to download or watch any BBC programmes on iPlayer."
        },
        {
            "question": "How can I request an official student letter from the university?",
            "ground_truth": "You can request various official student letters through the 'Letters and Documents' section of your online Student Record."
        },
        {
            "question": "What are the different ways I can make a payment to the university?",
            "ground_truth": "You can make a payment to the university online via the student portal, through bank transfer, or using services like Convera."
        },
        {
            "question": "Can I work on a placement year with my Student visa?",
            "ground_truth": "Yes, if the placement is an integral and assessed part of your course, you can work on a placement year with your Student visa."
        },
        {
            "question": "What information is included in the 'Welcome to the UK' guide for international students?",
            "ground_truth": "The 'Welcome to the UK' guide contains essential information for international students, including details on immigration, healthcare, banking, and adjusting to life in the UK."
        },
        {
            "question": "When is the earliest I can apply to extend my Student visa from within the UK?",
            "ground_truth": "You can apply to extend your Student visa up to 3 months before your current visa expires."
        },
        {
            "question": "What is the cost to use the laundry machines on campus?",
            "ground_truth": "The cost for laundry services can be found on the provider's app or website, which is mentioned in the university's laundry guide."
        },
        {
            "question": "What kind of support can the Careers and Employment service offer me?",
            "ground_truth": "The Careers and Employment service offers support with CVs, applications, interview skills, finding part-time jobs, and career planning."
        },
        {
            "question": "If I am unhappy with my accommodation, who is the first person I should talk to?",
            "ground_truth": "If you are unhappy in your accommodation, you should first speak with your Resident Assistant or contact the Accommodation Team to discuss the issues."
        },
        {
            "question": "What is the process for making a payment to the university from overseas?",
            "ground_truth": "International students can make payments through the university's online portal or use services like Convera (formerly Western Union Business Solutions) for bank transfers."
        },
        {
            "question": "Are there specific times when I can apply to change my room?",
            "ground_truth": "Yes, applications to change accommodation are typically only open during specific periods, which are advertised by the accommodation office."
        },
        {
            "question": "What kind of visa is required for a student to stay and work in the UK after graduation?",
            "ground_truth": "Students who wish to stay and work in the UK after graduation can apply for the Graduate Route, also known as the Post-Study Work visa."
        },
        {
            "question": "Will I be charged for a replacement ID card if it was stolen and I have a police crime reference number?",
            "ground_truth": "The university may waive the £15 replacement fee for a stolen ID card if you provide a valid police crime reference number."
        }
        
    ]