from dria_workflows import Workflow, WorkflowBuilder, Operator, Write, Edge
from dria.factory.utilities import get_abs_path


def validate_prediction(prediction: str, correct_answer: str) -> Workflow:
    """
    Generate a Task to determine if the predicted answer is contextually and semantically correct compared to the correct answer.

    :param prediction: The predicted answer to be evaluated.
    :param correct_answer: The correct answer to compare against.
    :return: A Task object representing the workflow.
    """

    # Initialize the workflow with variables
    builder = WorkflowBuilder(prediction=prediction, correct_answer=correct_answer)

    # Add a generative step using the prompt
    builder.generative_step(
        path=get_abs_path("validate.md"),
        operator=Operator.GENERATION,
        outputs=[Write.new("validation_result")],
    )

    # Define the flow of the workflow
    flow = [Edge(source="0", target="_end")]
    builder.flow(flow)

    # Set the return value of the workflow
    builder.set_return_value("validation_result")
    return builder.build()


def evaluate_prediction(prediction: str, question: str, context: str) -> Workflow:
    """
    Generate a Task to determine if the predicted answer is contextually and semantically correct compared to the correct answer.

    :param prediction: The predicted answer to be evaluated.
    :param question: The question to compare against.
    :param context: The context to compare against.
    :return: A Task object representing the workflow.
    """

    # Initialize the workflow with variables
    builder = WorkflowBuilder(prediction=prediction, question=question, context=context)

    # Add a generative step using the prompt
    builder.generative_step(
        path=get_abs_path("evaluate.md"),
        operator=Operator.GENERATION,
        outputs=[Write.new("evaluation_result")],
    )

    # Define the flow of the workflow
    flow = [Edge(source="0", target="_end")]
    builder.flow(flow)

    # Set the return value of the workflow
    builder.set_return_value("evaluation_result")
    return builder.build()
