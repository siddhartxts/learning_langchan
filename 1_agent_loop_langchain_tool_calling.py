from dotenv import load_dotenv

load_dotenv()

from langchain.chat_models import init_chat_model
from langchain.tools import tool
from langchain_core.messages import HumanMessage, SystemMessage, ToolMessage
from langsmith import traceable

MAX_ITERATIONS = 10
MODEL = "gpt-4o-mini"


# --- Tools (LangChain @tool decorator) ---


@tool
def get_product_price(product: str) -> float:
    """Look up the price of a product in the catalog.

    The catalog contains exactly three products. The `product` argument must be
    one of these exact lowercase names: "laptop", "headphones", "keyboard".
    There are no brands or variants — "laptop" is a complete, valid product name.

    Returns the price in dollars as a float.
    """
    print(f"    >> Executing get_product_price(product='{product}')")
    prices = {"laptop": 1299.99, "headphones": 149.95, "keyboard": 89.50}
    return prices.get(product.lower().strip(), 0)


@tool
def apply_discount(price: float, discount_tier: str) -> float:
    """Apply a discount tier to a price and return the final discounted price.

    The `discount_tier` argument must be one of these exact lowercase names:
    "bronze", "silver", "gold". These are complete, valid tier names — no
    membership number or other detail is needed.

    The `price` argument must be a price previously returned by
    get_product_price. Always call get_product_price before calling this tool.
    """
    print(f"    >> Executing apply_discount(price={price}, discount_tier='{discount_tier}')")
    discount_percentages = {"bronze": 5, "silver": 12, "gold": 23}
    discount = discount_percentages.get(discount_tier.lower().strip(), 0)
    return round(price * (1 - discount / 100), 2)


# --- Agent Loop ---


@traceable(name="LangChain Agent Loop")
def run_agent(question: str):
    tools = [get_product_price, apply_discount]
    tools_dict = {t.name: t for t in tools}

    llm = init_chat_model(f"openai:{MODEL}", temperature=0)
    llm_with_tools = llm.bind_tools(tools)

    print(f"Question: {question}")
    print("=" * 60)

    messages = [
        SystemMessage(
            content=(
                "You are a helpful shopping assistant. "
                "You have access to a product catalog tool "
                "and a discount tool.\n\n"
                "CATALOG FACTS:\n"
                "- The only valid products are exactly: laptop, headphones, keyboard.\n"
                "- The only valid discount tiers are exactly: bronze, silver, gold.\n"
                "- There are no brands, models, or variants. If the user says "
                "'a laptop', that IS the exact catalog product 'laptop'. "
                "If the user says 'gold discount', that IS the exact tier 'gold'.\n\n"
                "STRICT RULES — you must follow these exactly:\n"
                "1. NEVER guess or assume any product price. "
                "You MUST call get_product_price first to get the real price.\n"
                "2. Only call apply_discount AFTER you have received "
                "a price from get_product_price. Pass the exact price "
                "returned by get_product_price — do NOT pass a made-up number.\n"
                "3. NEVER calculate discounts yourself using math. "
                "Always use the apply_discount tool.\n"
                "4. If the user's request already mentions a valid product AND "
                "a valid discount tier, do NOT ask any clarifying questions — "
                "call the tools immediately.\n"
                "5. Only ask a clarifying question if the product or discount "
                "tier is genuinely missing or is not in the valid lists above."
            )
        ),
        HumanMessage(content=question),
    ]

    for iteration in range(1, MAX_ITERATIONS + 1):
        print(f"\n--- Iteration {iteration} ---")

        ai_message = llm_with_tools.invoke(messages)

        tool_calls = ai_message.tool_calls

        print(f"  [DEBUG] ai_message.content: {ai_message.content!r}")
        print(f"  [DEBUG] ai_message.tool_calls: {tool_calls}")

        # If no tool calls, this is the final answer
        if not tool_calls:
            print(f"\nFinal Answer: {ai_message.content}")
            return ai_message.content

        messages.append(ai_message)

        # Answer EVERY tool call in this message. The OpenAI API rejects the
        # next request if any tool_call_id is left without a ToolMessage.
        for tool_call in tool_calls:
            tool_name = tool_call.get("name")
            tool_args = tool_call.get("args", {})
            tool_call_id = tool_call.get("id")

            print(f"  [DEBUG] selected tool name: {tool_name}")
            print(f"  [DEBUG] selected tool args: {tool_args}")

            tool_to_use = tools_dict.get(tool_name)
            if tool_to_use is None:
                raise ValueError(f"Tool '{tool_name}' not found")

            observation = tool_to_use.invoke(tool_args)

            print(f"  [DEBUG] tool result: {observation}")

            messages.append(
                ToolMessage(content=str(observation), tool_call_id=tool_call_id)
            )

    print("ERROR: Max iterations reached without a final answer")
    return None


if __name__ == "__main__":
    print("Hello LangChain Agent (.bind_tools)!")
    print()
    result = run_agent("What is the price of a laptop after applying a gold discount?")