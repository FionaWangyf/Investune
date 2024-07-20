
import streamlit as st
import time

st.header("Our Users Community")
st.subheader("Post your updates on in!")
# name = st.chat_input("Your name to display.")
if "messages" not in st.session_state:
    st.session_state.messages = []

# for message in st.session_state.messages:
#     with st.chat_message(message["name"]):
#         st.write(message["content"])
#         # st.markdown(message["content"])

namee = st.text_input("Enter your name:")
# prompt = st.chat_input("Write a stock message to the community!")

for message in st.session_state.messages:
    with st.chat_message(message["name"]):
        # st.markdown(f":rainbow[*{message["name"]}*]")
        # st.write(message["content"])
        st.write(f""":rainbow[*{message["name"]}*]  
                     {message["content"]}""")
        # st.markdown(message["content"])


if namee:
    # prompt = st.chat_input("Write a stock message to the community!")
    with st.chat_message(namee):
        prompt = st.chat_input("Write a stock message to the community!")
        # prompt = st.chat_input("Write a stock message to the community!")
    if prompt:
        with st.chat_message("ai", avatar="🙏🏻"):
            st.markdown(f"Dear {namee},")
            st.write("thankyou for adding your post to our community! We hope you get benefited from posts here as well!")

        st.session_state.messages.append({"name": namee, "content": prompt})
        # with st.chat_message("ai", avatar="🙏🏻"):
        #     st.markdown(f"Dear {namee},")
        #     st.write("thankyou for adding your post to our community! We hope you get benefited from posts here as well!")
        time.sleep(3)
        st.rerun()
        # st.markdown("WAY 1")
        # # st.markdown(f":rainbow[*{namee}*]")
        # with st.chat_message(namee):
        #     # st.markdown(prompt)
        #     st.markdown(f":rainbow[*{namee}*]")
        #     st.write(prompt)
        #     st.session_state.messages.append({"name": namee, "content": prompt})
      
        # st.markdown("WAY 2")
        with st.chat_message(namee):
            # st.markdown(prompt)
            # st.markdown(f":rainbow[*{namee}*]")
            st.write(f""":rainbow[*{namee}*]  
                     {prompt}""")
            st.session_state.messages.append({"name": namee, "content": prompt})

    # if prompt:
    #     with st.chat_message("ai", avatar="🙏🏻"):
    #         st.markdown(f"Dear {namee},")
    #         st.write("thankyou for adding your post to our community! We hope you get benefited from posts here as well!")
