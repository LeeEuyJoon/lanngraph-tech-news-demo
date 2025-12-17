from datetime import datetime

from dotenv import load_dotenv

from mini_agent import GraphState, Tech
from mini_agent.node.plan_collection import plan_collection

load_dotenv()


def test_plan_collection_node():
    print("test_plan_collection_node 실행")
    initial_state = GraphState(
        tech=Tech.SPRING,
        attempt=0,
        max_attempts=3,
        today=datetime.now().strftime("%Y-%m-%d"),
    )

    result = plan_collection(initial_state)

    print("Collection Plan 결과:")
    for idx, plan in enumerate(result["collection_plan"]):
        print(f"Plan {idx + 1}: {plan}")


if __name__ == "__main__":
    test_plan_collection_node()
