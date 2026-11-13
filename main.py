from bakery import assert_equal
from dataclasses import dataclass
from drafter import *


set_website_title("Chemistry Helper")
set_site_information(
    author="Keira Wynn",
    description="Chemistry Helper Website",
    sources = "",
    planning = [],
    links = ["https://github.com/klwynn/Chemistry-Helper"]
)
hide_debug_information()


MOLAR_MASSES = {
    "H2": 2.016,
    "O2": 32.00,
    "H2O": 18.015,
    "CH4": 16.04,
    "CO2": 44.01,
    "NaCl": 58.44,
    "Na": 22.99,
    "Cl2": 70.90
}


@dataclass
class PracticeQuestion:
    question: str
    answer: str
    topic: str
    explanation: str


@dataclass
class State:
    page: str
    topic: str
    practice_questions: list[PracticeQuestion]
    score: int
    feedback: str


@route
def index(state: State) -> Page:
    '''
    This function displays the homepage and allows users
    to navigate to different chemistry topics.

    Args:
        state (State): The current website state.

    Returns:
        Page: The homepage with navigation buttons.
    '''
    state.page = "Home"
    state.topic = "Home"

    return Page(state, [
        Text("Chemistry Learning Tool"),
        Text("Choose a topic to get started!"),
        Button("Stoichiometry", "stoichiometry_page"),
        Button("Percent Yield", "percent_yield_page"),
        Button("Energy Changes", "energy_page"),
        Button("Practice Questions", "practice_page")
    ])



@route
def stoichiometry_page(state: State) -> Page:
    '''
    This function displays an introduction to stoichiometry
    and provides access to the limiting reactant calculator.

    Args:
        state (State): The current website state.

    Returns:
        Page: The stoichiometry introduction page.
    '''
    state.page = "Stoichiometry"
    state.topic = "Limiting Reactants"

    return Page(state, [
        Text("Stoichiometry and Mole Ratios"),
        Text("Use this calculator to find the limiting reactant."),
        Button("Calculate Limiting Reactants", "limiting_page"),
        Button("Back to Home", "index")
    ])



@route
def limiting_page(state: State) -> Page:
    '''
    This function displays the limiting reactant calculator
    and allows users to enter reactant formulas and masses.

    Args:
        state (State): The current website state.

    Returns:
        Page: The limiting reactant calculator page.
    '''
    state.page = "Limiting Reactants"

    return Page(state, [
        Text("Limiting Reactants Calculator"),
        Text("Enter your two reactants and their masses in grams."),
        Text("Reactant 1 Formula:"),
        TextBox("formula_1"),
        Text("Reactant 1 Mass (g):"),
        TextBox("mass_1", "1"),
        Text("Reactant 2 Formula:"),
        TextBox("formula_2"),
        Text("Reactant 2 Mass (g):"),
        TextBox("mass_2", "1"),
        Button("Calculate", "calculate_limiting"),
        Text(state.feedback),
        Button("Back to Home", "index"),
        Button("Next: Percent Yield", "percent_yield_page")
    ])


@route
def calculate_limiting(state: State, formula_1: str,
                       mass_1: float, formula_2: str,
                       mass_2: float) -> Page:
    '''
    This function calculates the moles of two reactants
    and determines which reactant is limiting.

    Args:
        state (State): The current website state.
        formula_1 (str): The chemical formula of the first reactant.
        mass_1 (float): The mass of the first reactant in grams.
        formula_2 (str): The chemical formula of the second reactant.
        mass_2 (float): The mass of the second reactant in grams.

    Returns:
        Page: The calculator page displaying the result or an error.
    '''
    if formula_1 not in MOLAR_MASSES or formula_2 not in MOLAR_MASSES:
        state.feedback = "Please enter valid chemical formulas."

    elif mass_1 <= 0 or mass_2 <= 0:
        state.feedback = "Masses must be greater than zero."

    else:
        molar_mass_1 = MOLAR_MASSES[formula_1]
        molar_mass_2 = MOLAR_MASSES[formula_2]

        moles_1 = mass_1 / molar_mass_1
        moles_2 = mass_2 / molar_mass_2

        if moles_1 < moles_2:
            limiting = formula_1
            excess = formula_2
            excess_grams = (moles_2 - moles_1) * molar_mass_2

        elif moles_2 < moles_1:
            limiting = formula_2
            excess = formula_1
            excess_grams = (moles_1 - moles_2) * molar_mass_1

        else:
            limiting = "Neither"
            excess = "None"
            excess_grams = 0

        state.feedback = (
            "Limiting Reactant: " + limiting
            + " | Excess Reactant: " + excess
            + " | Excess Remaining: "
            + str(round(excess_grams, 2)) + " g"
        )

    return limiting_page(state)


@route
def percent_yield_page(state: State) -> Page:
    '''
    This function displays the percent yield calculator
    and allows users to enter actual and theoretical yields.

    Args:
        state (State): The current website state.

    Returns:
        Page: The percent yield calculator page.
    '''
    state.page = "Percent Yield"
    state.topic = "Percent Yield"

    return Page(state, [
        Text("Percent Yield Calculator"),
        Text("Enter your actual and theoretical yields."),
        Text("Actual Yield (g):"),
        TextBox("actual", "1"),
        Text("Theoretical Yield (g):"),
        TextBox("theoretical", "1"),
        Button("Calculate", "calculate_yield"),
        Text(state.feedback),
        Button("Back to Home", "index"),
        Button("Next: Energy", "energy_page")
    ])


@route
def calculate_yield(state: State, actual: float,
                    theoretical: float) -> Page:
    '''
    This function calculates percent yield using the
    actual yield and theoretical yield entered by the user.

    Args:
        state (State): The current website state.
        actual (float): The actual yield in grams.
        theoretical (float): The theoretical yield in grams.

    Returns:
        Page: The percent yield page displaying the result or an error.
    '''
    if actual < 0 or theoretical <= 0:
        state.feedback = "Please enter valid positive yields."

    else:
        percent = (actual / theoretical) * 100
        state.feedback = "Percent Yield: " + str(round(percent, 2)) + "%"

    return percent_yield_page(state)


@route
def energy_page(state: State) -> Page:
    '''
    This function displays information about endothermic
    and exothermic reactions and provides an enthalpy calculator.

    Args:
        state (State): The current website state.

    Returns:
        Page: The energy changes page.
    '''
    state.page = "Energy"
    state.topic = "Enthalpy"

    return Page(state, [
        Text("Endothermic and Exothermic Reactions"),
        Text("Endothermic: Absorbs heat (positive ΔH)"),
        Text("Exothermic: Releases heat (negative ΔH)"),
        Text("Enter the enthalpy change:"),
        TextBox("delta_h", "0"),
        Button("Check Reaction Type", "check_energy"),
        Text(state.feedback),
        Button("Back to Home", "index"),
        Button("Next: Practice", "practice_page")
    ])


@route
def check_energy(state: State, delta_h: float) -> Page:
    '''
    This function determines whether a reaction is
    endothermic or exothermic based on its enthalpy change.

    Args:
        state (State): The current website state.
        delta_h (float): The enthalpy change entered by the user.

    Returns:
        Page: The energy page displaying the reaction type.
    '''
    if delta_h > 0:
        state.feedback = "This is an endothermic reaction."

    elif delta_h < 0:
        state.feedback = "This is an exothermic reaction."

    else:
        state.feedback = "There is no net enthalpy change."

    return energy_page(state)



@route
def practice_page(state: State) -> Page:
    '''
    This function displays chemistry practice questions
    and allows users to submit their answers.

    Args:
        state (State): The current website state.

    Returns:
        Page: The practice questions page.
    '''
    state.page = "Practice"
    state.topic = "Practice Questions"

    components = [
        Text("Chemistry Practice Questions")
    ]

    for question in state.practice_questions:
        components.append(Text(question.question))

    components.append(Text("Enter your answer:"))
    components.append(TextBox("user_answer"))
    components.append(Button("Submit Answer", "check_answer"))
    components.append(Text(state.feedback))
    components.append(Button("View Results", "results_page"))
    components.append(Button("Back to Home", "index"))

    return Page(state, components)


@route
def check_answer(state: State, user_answer: str) -> Page:
    '''
    This function checks the user's answer against the
    correct answer and updates their practice score.

    Args:
        state (State): The current website state.
        user_answer (str): The answer entered by the user.

    Returns:
        Page: The practice page displaying feedback.
    '''
    question = state.practice_questions[0]

    if user_answer.strip().upper() == question.answer.upper():
        state.score = 1
        state.feedback = "Correct! " + question.explanation

    else:
        state.score = 0
        state.feedback = "Incorrect. " + question.explanation

    return practice_page(state)


@route
def results_page(state: State) -> Page:
    '''
    This function calculates and displays the user's
    practice results, including correct and incorrect answers.

    Args:
        state (State): The current website state.

    Returns:
        Page: The practice results page.
    '''
    total = len(state.practice_questions)
    wrong = total - state.score

    return Page(state, [
        Text("Practice Results"),
        Text("Correct: " + str(state.score)),
        Text("Incorrect: " + str(wrong)),
        Text("Total Questions: " + str(total)),
        Button("Try Again", "practice_page"),
        Button("Back to Home", "index")
    ])


questions_list = [
    PracticeQuestion(
        question="What is the molar mass of H2O?",
        answer="18.015",
        topic="Molar Mass",
        explanation="Water contains two hydrogen atoms and one oxygen atom."
    )
]


initial_state = State(
    page="Home",
    topic="Home",
    practice_questions=questions_list,
    score=0,
    feedback=""
)

#Unit Tests
test_state = State("Home", "Home", questions_list, 0, "")
page = index(test_state)
assert_equal(page.state.page, "Home")

test_state = State("Home", "Home", questions_list, 0, "")
page = stoichiometry_page(test_state)
assert_equal(page.state.topic, "Limiting Reactants")

test_state = State("Home", "Home", questions_list, 0, "")
page = limiting_page(test_state)
assert_equal(page.state.page, "Limiting Reactants")

test_state = State("Home", "Home", questions_list, 0, "")
page = calculate_limiting(test_state, "H2", 4.032, "O2", 32.0)
assert_equal(test_state.feedback,
             "Limiting Reactant: O2 | Excess Reactant: H2 | Excess Remaining: 2.02 g")

test_state = State("Home", "Home", questions_list, 0, "")
page = calculate_limiting(test_state, "ABC", 5.0, "O2", 10.0)
assert_equal(test_state.feedback, "Please enter valid chemical formulas.")

test_state = State("Home", "Home", questions_list, 0, "")
page = percent_yield_page(test_state)
assert_equal(page.state.page, "Percent Yield")

test_state = State("Home", "Home", questions_list, 0, "")
page = calculate_yield(test_state, 8.0, 10.0)
assert_equal(test_state.feedback, "Percent Yield: 80.0%")

test_state = State("Home", "Home", questions_list, 0, "")
page = energy_page(test_state)
assert_equal(page.state.topic, "Enthalpy")

test_state = State("Home", "Home", questions_list, 0, "")
page = check_energy(test_state, 25.0)
assert_equal(test_state.feedback,
             "This is an endothermic reaction.")

test_state = State("Home", "Home", questions_list, 0, "")
page = check_energy(test_state, -25.0)
assert_equal(test_state.feedback,
             "This is an exothermic reaction.")

test_state = State("Home", "Home", questions_list, 0, "")
page = practice_page(test_state)
assert_equal(page.state.page, "Practice")

test_state = State("Home", "Home", questions_list, 0, "")
page = check_answer(test_state, "18.015")
assert_equal(test_state.score, 1)

test_state = State("Home", "Home", questions_list, 0, "")
page = check_answer(test_state, "20")
assert_equal(test_state.score, 0)

test_state = State("Home", "Home", questions_list, 1, "")
page = results_page(test_state)
assert_equal(page.content[0], Text("Practice Results"))


start_server(initial_state)

