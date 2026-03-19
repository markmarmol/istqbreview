# Hardcoded Quiz Questions
QUIZ_QUESTIONS = [
    {
        "question": "When the tester verifies the test basis while designing tests early in the lifecycle, which testobjective is being achieved?",
        "options": [
            "Gaining confidence",
            "Finding defects",
            "Evaluating work products",
            "Providing information for decision making"
        ],
        "correct_answer": "C",
        "explanation": "In some Agile teams, people are encouraged to use their skills to help the team, regardless of their role. This could mean that testers help the developers write code and developers help tesers test. What is this approach called?"
    },
    {
        "question": "In some Agile teams, people are encouraged to use their skills to help the team, regardless of their role. This could mean that testers help the developers write code and developers helptesters test. What is this approach called?",
        "options": [
            "Team Aid",
            "Whole Team",
            "Skills First",
            "First Aid"
        ],
        "correct_answer": "B",
        "explanation": "B is correct. This is an example of the Whole Team approach where the team members leveragetheir skills, regardless of roles, to accomplish the goals of the team.."
    },
    {
        "question": "Which of the following is a correct statement?",
        "options": [
            "A developer makes a mistake which causes a defect that may be seen as a failure during dynamic testing",
            "A developer makes an error which results in a failure that may be seen as a fault when the software is executed",
            "A developer has introduced a failure which results in a defect that may be seen as a mistake during dynamic testing",
            "A developer makes a mistake which causes a bug that may be seen as a defect when the software is executed"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. The developer makes a mistake/error which causes a defect/fault/bug which may cause a failure when the code is dynamically tested or executed.
        B is incorrect because fault and failure are reversed.
        C is incorrect because failure and mistake are reversed.
        D is incorrect because it's a failure that's seen during execution, not the defect itself. The failure is a symptom of the defect."""
    },
    {
        "question": "Why is it important to avoid the principle of tests wearing out?",
        "options": [
            "Dynamic testing is less reliable in finding bugs",
            "Running the same tests repeatedly will consistently find new failures",
            "Tests should not be context dependent",
            "Running the same tests repeatedly will reduce the chance of finding new failures"
        ],
        "correct_answer": "D",
        "explanation": """D is correct. As tests are run repeatedly, the tests become less effective.
        A is not correct because dynamic testing should be used and helps to alleviate tests wearing out.
        B is not correct. The same tests do wear out.
        C is not correct because testing should be context dependent."""
    },
    {
        "question": "When following a standard test process, when should the test control activity take place?",
        "options": [
            "During the planning activities",
            "During the implementation and execution activities",
            "During the monitoring activities",
            "During all the activities"
        ],
        "correct_answer": "D",
        "explanation": """D is correct. Control occurs throughout the project to ensure that it is staying on track based on
the plan and to take any corrective steps that may be necessary. The monitoring information is
used to determine if control actions are needed."""
    },
    {
        "question": "Which of the following is the activity that compares the planned test progress to the actual test progress?",
        "options": [
            "Test monitoring",
            "Test planning",
            "Test closure",
            "Test control"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. Test monitoring involves the on-going comparison of actual progress against the test plan.
B is incorrect because it defines testing objectives.
C is incorrect because the activities have already completed and the project is closing down.
D is incorrect because test control is when you take actions to correct any issues observed during
monitoring."""
    },
    {
        "question": " If you are working on a project that is constrained by time and budget, which is pressuring testing to be done quickly. How should the test approach be adjusted?",
        "options": [
            "Develop detailed test cases to reduce the test automation effort",
            "Use techniques such as exploratory and checklist testing to spend less time on test case development",
            "Ensure that your testing starts only after the developers have completed integration tests",
            "Develop end-to-end test automation before performing manual testing so the automation can be used sooner"
        ],
        "correct_answer": "B",
        "explanation": """B is correct. These techniques will help adjust to the project context where there is pressure to
test quickly. These are lightweight approaches that require less time preparing documentation
and allow test execution to start sooner.
A is not correct because developing detailed test cases will take significant time.
C is not correct because starting testing earlier would be helpful, not later.
D is not correct because this will be problematic automation and the automators will be slowed down by
the failures that would have been found in manual testing."""
    },
    {
        "question": "What is the biggest problem with a developer testing his own code?",
        "options": [
            "Developers are not good testers",
            "Developers are not quality focused",
            "Developers are not objective about their own code",
            "Developers do not have time to test their own code"
        ],
        "correct_answer": "C",
        "explanation": """C is correct. This is the biggest problem because developers have biases toward the accuracy
and implementation of their own code. Testers and developers think differently and testers can be
more objective as they are not invested in the code.
A and B are not necessarily true, some developers are good testers and have a good quality focus.
D is not correct because unit testing is part of their job and time should be made in the schedule for at
least unit testing."""
    },
    {
        "question": "Which of the following is an example of a good testing practice?",
        "options": [
            "Testers should have development experience",
            "Developers should determine the order of test execution in the test procedures",
            "Test design should begin when the code is complete to avoid changes",
            "Testers should review requirements documents as soon as a readable draft is available"
        ],
        "correct_answer": "D",
        "explanation": """D is correct. This is a good testing practice.
A is not a requirement for many testers.
B is not correct because this should be determined by the testers based on priority, risk, availability, etc.
C is not correct because test design should start during code design and implementation."""
    },
    {
        "question": "When coding is directed by the test cases, what development approach is being used?",
        "options": [
            "TDD",
            "BDD",
            "ATDD",
            "TBD"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. This is an example of test-driven development."""
    },
    {
        "question": "During which level(s) of testing should non-functional tests be executed?",
        "options": [
            "Unit and integration only",
            "System testing only",
            "Integration, system and acceptance only",
            "Unit, integration, system and acceptance only"
        ],
        "correct_answer": "D",
        "explanation": """D is correct. Non-functional tests can and should be executed at all levels of testing."""
    },
    {
        "question": "When a system is targeted for decommissioning, what type of maintenance testing may be required?",
        "options": [
            "Retirement testing",
            "Regression testing",
            "Data migration testing",
            "Patch testing"
        ],
        "correct_answer": "C",
        "explanation": """C is correct, per syllabus. Data migration to another system or data migration to an archival
system may be needed.
A is incorrect, there is no such testing type.
B is incorrect because this is more appropriate for current systems, not the system being retired.
D is incorrect because this is of no use for a system being retired."""
    },
    {
        "question": " In an iterative lifecycle model, which of the following is an accurate statement about testing activities?",
        "options": [
            "For every development activity, there should be a corresponding testing activity",
            "For every testing activity, appropriate documentation should be produced, versioned and stored",
            "For every development activity resulting in code, there should be a testing activity to document test cases",
            "For every testing activity, metrics should be recorded and posted to a metrics dashboard for all stakeholders"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. For any lifecycle model, this is a correct statement.
B is not correct because some testing activities may not produce documentation, such as reviews.
C is not correct because test cases are not always written, particularly in an Agile lifecycle (which is an
iterative lifecycle) where only exploratory testing might be used.
D is not correct because not all testing activities produce metrics (such as test case creation, reviews,
etc.) and, even if they did, not all stakeholders would be interested in those metrics."""
    },
    {
        "question": "In what way is CI/CD an example of the concept of shift-left?",
        "options": [
            "It gets the code to production faster",
            "It allows the developers to continuously integrate their code",
            "It requires continuous testing throughout the pipeline",
            "It elevates the testers as the owners of quality"
        ],
        "correct_answer": "C",
        "explanation": """C is correct. CI/CD requires continuous testing, including test automation, to be implemented for the
entire pipeline. This starts testing as early as possible and shifts it to the left in the timeline.
A is not correct as this is not a shift-left concept.
B is true of CI/CD implementations but does not shift-left the testing.
D is not correct because in a good CI/CD implementation, everyone owns quality."""
    },
    {
        "question": "In a formal review, which role is normally responsible for documenting all the open issues?",
        "options": [
            "The facilitator",
            "The author",
            "The scribe",
            "The manager"
        ],
        "correct_answer": "C",
        "explanation": """C is correct. The scribe is normally responsible for documenting all issues, problems and open
points. The author may take notes as well, but that is not their primary role."""
    },
    {
        "question": "What is the primary reason to get early and frequent feedback from stakeholders regarding a product being developed?",
        "options": [
            "To make them feel involved",
            "To ensure that their vision for the product will be realized",
            "To create more meetings",
            "To use the stakeholders as testers"
        ],
        "correct_answer": "B",
        "explanation": """B is correct per the syllabus. By getting their feedback, the team can ensure that what they are building is
what the stakeholders want.
A is not correct because, although it may be beneficial to have them feel a part of the team, it isn’t the
primary reason to get their feedback.
C is not correct because no one needs more meetings.
D is not correct although stakeholders may be used for UAT. Their feedback is needed much earlier than
UAT."""
    },
    {
        "question": "Which of the following is a benefit of static analysis?",
        "options": [
            "Defects can be identified that might not be caught by dynamic testing",
            "Early defect identification requires less documentation",
            "Early execution of the code provides a gauge of code quality",
            "Tools are not needed because reviews are used instead of executing code"
        ],
        "correct_answer": "A",
        "explanation": """A is correct, per syllabus. Static analysis with a static analyzer can be used to find defects such
as uninitialized variables that could be difficult to catch with dynamic testing.
B is incorrect because defects will still need to be documented regardless of how early they are found.
C is incorrect because this is dynamic analysis.
D is incorrect because static analysis usually requires the use of tools."""
    },
    {
        "question": "For a formal review, at what point in the process are the exit criteria defined?",
        "options": [
            "Planning",
            "Review initiation",
            "Individual review",
            "Fixing and reporting"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. The entry and exit criteria should be defined during the planning step in the review
process. These should be evaluated at each step to ensure the product is ready for the next step
in the process.
B, C and D are not correct because the criteria should already be defined by this point."""
    },
    {
        "question": "Which of the following test techniques uses the requirements specifications as a test basis?",
        "options": [
            "Structure-based",
            "Black-box",
            "White-box",
            "Exploratory"
        ],
        "correct_answer": "B",
        "explanation": """B is correct, per syllabus. Black-box testing is based off the requirements documents.
A and C are incorrect because these use the structure of the software as the test basis.
D is incorrect because exploratory testing is often done when there is no specification, thus giving the
tester the opportunity to learn about the software while testing."""
    },
    {
        "question": "If you are testing a module of code, how do you determine the level of branch coverage you have achieved?",
        "options": [
            "By taking the number of branches you have tested and dividing that by the total number of executable statements in the module",
            "By taking the number of branches you have tested and dividing that by the total number of branches in the module",
            "By taking the number of branches you have tested and dividing that by the total lines of code in the module",
            "By taking the number of branches you have tested and dividing that by the total number of test cases you have executed for the module"
        ],
        "correct_answer": "B",
        "explanation": """B is correct. Branch coverage looks at the number of branches tested versus the number of
branches in the code under test."""
    },
    {
        "question": "If you have a section of code that has one simple IF statement, how many tests will be needed to achieve 100%% branch coverage?",
        "options": [
            "1",
            "2",
            "5",
            "Unknown with this information"
        ],
        "correct_answer": "B",
        "explanation": """B is correct. A simple IF statement will be composed of If ... then ... else.... end if. There are two
branch outcomes, one for the result of the If being true and one for it being false. Since 100%
branch coverage requires at least one test case for each branch outcome, two tests are needed.
A and C are incorrect because these are the wrong numbers of tests.
D would be correct if this weren’t defined as a simple if statement because a complex if statement could
include more than two outcomes."""
    },
    {
        "question": "Which of the following is a good reason to use experience-based testing?",
        "options": [
            "You can find defects that might be missed by more formal techniques",
            "You can test for defects that only experienced users would encounter",
            "You can target the developer’s efforts to the areas that users will be more likely to use",
            "It is supported by strong tools and can be automated"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. Experience-based testing is often used to fill in the gaps left by the more formal
testing techniques.
B is not correct because it is used by experienced testers and has nothing to do with the experience level
of the users.
C is not correct because it is a test technique, not a development technique.
D is not correct. There is not much tool support for these techniques and automation is not usually a goal
because the effectiveness depends on the experience of the tester."""
    },
    {
        "question": "What is error guessing?",
        "options": [
            "A testing technique used to guess where a developer is likely to have made a mistake",
            "A technique used for assessing defect metrics",
            "A development technique to verify that all error paths have been coded",
            "A planning technique used to anticipate likely schedule variances due to faults"
        ],
        "correct_answer": "A",
        "explanation": """A is correct. Error guessing is a technique used to anticipate where developers are likely to make
errors and to create tests to cover those areas."""
    },
    {
        "question": "When using the 3 C’s technique for user story development, what is the work product that is created for the Confirmation aspect?",
        "options": [
            "Test Approach",
            "Acceptance Criteria",
            "Entry Criteria",
            "Exit Criteria"
        ],
        "correct_answer": "B",
        "explanation": """B is correct. The confirmation aspect of the 3 C’s is the acceptance criteria."""
    },
    {
        "question": """You are testing a machine that scores exam papers and assigns grades. Based on the score achieved the grades are as follows: 1-49 = F, 50-59 = D-, 60-69 = D, 70-79 = C, 80-89 =B, 90-100=A
       
         If you apply equivalence partitioning, how many test cases will you need to achieve minimum test coverage?
        """,
        "options": [
            "6",
            "8",
            "10",
            "12"
        ],
        "correct_answer": "B",
        "explanation": """B is correct. You need a test for the invalid too low (0 or less), one for each valid partition, and one
for invalid too high (>100). It may not allow you to enter a value > 100, but it should be tested to
make sure it provides a proper error."""
    },
    {
        "question": """You are testing a thermostat for a heating/air conditioning system. You have been given the following requirements:
        
        • When the temperature is below 70 degrees, turn on the heating system
        • When the temperature is above 75 degrees, turn on the air conditioning system
        • When the temperature is between 70 and 75 degrees, inclusive, turn on fan only
        
       Which of the following is the minimum set of test temperature values to achieve 100% two-value boundary value analysis coverage?""",
        "options": [
            "70, 75",
            "65, 72, 80",
            "69, 70, 75, 76",
            "70, 71, 74, 75, 76"
        ],
        "correct_answer": "C",
        "explanation": """C is correct.

For the heating system, the values to test are 69, 70
For the air conditioning system, the values are 75, 76
For the fan only, the values are 69, 70, 75, 76

<-- 69 | 70 – 75 | 76 -->

The proper test set combines all these values, 69, 70, 75, 76"""
    },
    {
        "question": """You have been given the following conditions and results from those condition combinations. Given this information, using the decision table technique, what is the minimumnumber of test cases you would need to test these conditions?
        
        
        Conditions:
            Valid cash
            Valid credit card
            Valid debit card
            Valid pin
            Bank accepts
            Valid Selection
            Item in Stock

        Results:
            Reject Cash
            Reject Card
            Error Message
            Return Cash
            Refund Card
            Sell Item
        """,
        "options": [
            "7",
            "13",
            "15",
            "18"
        ],
        "correct_answer": "C",
        "explanation": """C is correct. See table below.
![Decision Table](images/image1.png)"""
    }
    ,
    {
        "question": "",
        "options": [
            "",
            "",
            "",
            ""
        ],
        "correct_answer": "",
        "explanation": """"""
    }
]
