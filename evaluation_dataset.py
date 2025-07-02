# evaluation_dataset.py

def get_evaluation_dataset():
    """
    Returns a list of dictionaries, where each dictionary contains a question
    and the "ground truth" answer based on the content from ask.herts.ac.uk.
    """
    return [
        {
            "question": "How much does it cost to replace a lost or damaged student ID card?",
            "ground_truth": "The fee for a replacement ID card is £10."
        },
        {
            "question": "What should I do if my ID card is stolen?",
            "ground_truth": "If your ID card is stolen, you should report it to the police to get a crime reference number. The university may waive the replacement fee if you provide this number. Report to Lost or stolen ID cards should be reported to the Library and Computing Services at helpdesk@herts.ac.uk at the earliest opportunity to prevent others from using your card until you get a replacement."
        },
        {
            "question": "Can I get a temporary ID slip for my exams?",
            "ground_truth": "Yes, you can obtain a temporary ID slip for exams from the Ask Herts Helpdesk if you have lost your card. It is valid for 1 week from the date of issue"
        },
        {
            "question": "What is the current application fee for a Student Visa from outside the UK?",
            "ground_truth": "The application fee for a Student Visa made from outside the UK is £524."
        },
        # {
        #     "question": "How much is the accommodation deposit?",
        #     "ground_truth": "The accommodation deposit is £400, which serves as an advance payment of rent."
        # },
        {
            "question": "What are the steps to request an accommodation refund?",
            "ground_truth": "There are three steps: First, check your eligibility by contacting finance-accomm@herts.ac.uk, especially if you have overpaid, withdrawn, or suspended studies. Second, you must fill out an accommodation refund form, keeping in mind the refund will go to the original account. Third, submit the completed form via email to finance-accomm@herts.ac.uk."
        },
        {
            "question": "Which students are generally eligible for Council Tax exemption, and how does living arrangement affect it?",
            "ground_truth": "Full-time students on a course lasting at least six months are eligible. Part-time students with over 90 credits may also be eligible after a review. The exemption status of the property depends on who you live with; if all residents are exempt students, the entire household is exempt, but if you live with non-students, you may only receive a discount."
        },
        {
            "question": "Is it possible to change my allocated accommodation room?",
            "ground_truth": "Yes, you can apply to change your accommodation, but this is subject to availability and specific application periods."
        },
        {
            "question": "What is the step-by-step process for a fully registered, full-time University of Hertfordshire student to get their Council Tax exemption evidence?",
            "ground_truth": "First, request the exemption evidence through the Student Letters portal. Second, wait up to 20 minutes for the evidence to be emailed to your personal address. Third, download and save the evidence. Finally, submit the evidence to your local council according to their specific instructions."
        },
        {
            "question": "Who can I speak to if I am unhappy with my on-campus accommodation, both during and outside of office hours?",
            "ground_truth": "During office hours on weekdays, you can speak in person with the Residence Life and Safeguarding Team on either campus, email them at reslife@herts.ac.uk, or call them. You can also speak with Counselling services. Outside of office hours, you can contact a Resident Assistant (RA) using the non-emergency security number."
        },
        {
            "question": "Are there laundry facilities on campus?",
            "ground_truth": "Yes, laundry facilities are available on both the College Lane(07:00-23:00) and de Havilland(07:00-22:00) campuses."
        },
        {
            "question": "As a current student, what is the first step to engage with the Careers and Employment Service and what key resources are available?",
            "ground_truth": "The first step is to log into the Careers and Employment website. This gives you access to the Handshake community for live vacancies and appointments, and to e-learning programs on 'My Career Plan' to help develop employability skills."
        },
        {
            "question": "How do students access the Handshake platform and what can they use it for?",
            "ground_truth": "Students do not need to register for Handshake as an account is automatically created for them. They can use it to search for jobs, internships, and placements, and to book appointments, such as for a CV check."
        },
        {
            "question": "For how long after graduating can alumni use the Careers and Employment Service, and what is the quickest way to contact the team for support?",
            "ground_truth": "Graduates can receive support for up to 4 years after their course ends. To get instant support, you can use the Live Chat feature on the careers website by clicking the icon in the bottom right-hand corner."
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
            "question": "Under what circumstances do I need my own TV Licence if I live in on-campus accommodation versus a privately rented house?",
            "ground_truth": "If you live in on-campus accommodation, your individual room needs its own TV Licence to watch live TV or BBC iPlayer. In a privately rented house with a joint tenancy agreement, you likely only need one licence for the whole house. However, if you have a separate tenancy agreement for your own room, you will need your own licence."
        },
        {
            "question": "How to request a student letter?",
            "ground_truth": "First, they must ensure their details on their Student Record are correct. Then, they complete a specific form to request the letter. The letter will be sent to their personal email address in about 15 minutes."
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
            "question": "How do I request to move rooms, and what is the process if I want to leave my accommodation contract early?",
            "ground_truth": "To request a room move, you must email accommodation@herts.ac.uk with your details, which costs £25 and is subject to checks. To leave early, you need to request it via the 'Early Departure' link on the accommodation portal, but you are liable for the fees until the room is re-let."
        },

        {
            "question": "What are the different ways I can pay my tuition or accommodation fees, and are there any restrictions for in-person payments?",
            "ground_truth": "You can pay fees online using Flywire for various local payment methods, Convera for bank transfers in your local currency, or directly via the university's portal with a credit or debit card. You can also pay in person at the Place2Pay on the College Lane Campus, but they do not accept cash, cheques, or AMEX, and you cannot use a third person's card."
        }
        
    ]