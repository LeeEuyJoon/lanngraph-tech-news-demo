from mini_agent import GraphState, SourceType

def collect_events(state: GraphState) -> GraphState:
    """ 이벤트 수집 노드 (raw events 수집) """
    
    plans = state.get("collection_plan", [])
    raw_events = []
    
    for plan in plans:
        