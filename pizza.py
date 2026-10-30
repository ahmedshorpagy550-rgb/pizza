import google.generativeai as ai
import streamlit as st

pizza_menu = {
    "Margerita Pizza": {
        "image": "https://www.papajohnsegypt.com/images/Products/product_50_1768290827.jpg",
        "prices": {"Small": 140, "Medium": 180, "Large": 200},
        "key": "mrg"
    },
    "Chicken Ranch": {
        "image": "https://www.papajohnsegypt.com/images/Products/Chicken-Ranch---Spicy-Korean.jpg",
        "prices": {"Small": 170, "Medium": 200, "Large": 230},
        "key": "rch"
    },
    "Pepperoni Pizza": {
        "image": "https://www.papajohnsegypt.com/images/Products/product_9_1768291533.jpg",
        "prices": {"Small": 180, "Medium": 220, "Large": 250},
        "key": "ppr"
    }
}

pasta_menu = {
    "Alfredo Pasta": 150,
    "Chicken Pasta": 170,
    "Tomato Pasta": 120
}

drinks_menu = {
    "Cola": 30,
    "Orange Juice": 40,
    "Water": 15
}
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
st.header("Pizza Ordering Application")
st.title("Welcome to the Pizza Ordering App", text_alignment="center")
api_key = st.text_input("enter your api key here", type = "password")
if api_key:
    ai.configure(api_key=api_key)
    model = ai.GenerativeModel("gemini-pro")
burgers_tab, pizzas_tab, ice_coffee_tab, chatbot_tab = st.tabs(["Burgers", "Pizzas", "ice coffee", "Chat with PizzaBot"])
st.subheader("Order your favorite pizza now!")
with burgers_tab:
    st.header("this is the Burgers menu")
    st.write("Welcome to the Burgers tab!")
    col1, col2 = st.columns(2)
    with col1:
        st.image("https://i.pinimg.com/736x/62/58/54/6258543c0fddc0895e038f0a004d54e5.jpg")
    with col2:
        st.image("https://i.pinimg.com/736x/6c/86/9a/6c869ae8913a86daf3f3c8714a81d2ef.jpg")
with pizzas_tab:
    st.header("this is the Pizzas menu")
    st.write("Welcome to the Pizzas tab!")
with ice_coffee_tab:
    st.header("this is the Ice Coffee menu")
    st.write("Welcome to the Ice Coffee tab!")
with chatbot_tab:
    st.header("🤖 Chat with PizzaBot")
    st.write("Ask me about our menu, prices, or pizza recommendations!")

    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.write(message["content"])

    question = st.chat_input("Ask PizzaBot a question...")

    if question:
        st.session_state.chat_history.append({
            "role": "user",
            "content": question
        })

        with st.chat_message("user"):
            st.write(question)

        if not api_key:
            st.warning("Please enter your Gemini API key in the sidebar.")
        else:
            try:
                model = ai.GenerativeModel("gemini-3.5-flash")

                conversation = (
                    "You are PizzaBot, a friendly chatbot for a pizza restaurant. "
                    "Answer simply and briefly, especially for kids. "
                    "Help users with menu items, prices, and recommendations. "
                    f"Pizza menu: {pizza_menu}. "
                    f"Pasta menu: {pasta_menu}. "
                    f"Drinks menu: {drinks_menu}. "
                    f"Customer question: {question}"
                )

                with st.chat_message("assistant"):
                    with st.spinner("PizzaBot is thinking..."):
                        response = model.generate_content(conversation)
                        answer = response.text
                        st.write(answer)

                st.session_state.chat_history.append({
                    "role": "assistant",
                    "content": answer
                })

            except Exception:
                st.error("PizzaBot couldn't answer. Please check your API key.")

    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()