# admin.py
import streamlit as st
import pandas as pd
import json
import os
from memory import load_users
from knowledge_base import load_knowledge, save_knowledge

st.set_page_config(page_title="AI Bot Admin", layout="wide")

st.title("🤖 Панель управления ИИ-ботом")

tab1, tab2 = st.tabs(["📋 Контакты (Лиды)", "🧠 База знаний"])

with tab1:
    st.header("Собранные контакты")
    users = load_users()
    
    if not users:
        st.info("Пока нет данных.")
    else:
        # Convert to list of dicts for DataFrame
        data = []
        for uid, udata in users.items():
            data.append({
                "ID": uid,
                "Имя": udata.get("name"),
                "Никнейм": f"@{udata.get('username')}" if udata.get('username') else "-",
                "Телефон": udata.get("contact_info"),
                "Последнее сообщение": udata.get("history")[-1]["content"] if udata.get("history") else ""
            })
        
        df = pd.DataFrame(data)
        st.dataframe(df, use_container_width=True)
        
        if st.button("Обновить таблицу"):
            st.rerun()

with tab2:
    st.header("Редактирование базы знаний")
    
    knowledge = load_knowledge()
    
    # Intro
    st.subheader("Приветствие")
    new_intro = st.text_area("Текст приветствия", value=knowledge.get("intro", ""), height=100)
    
    # Benefits
    st.subheader("Преимущества (список)")
    benefits_text = "\n".join(knowledge.get("benefits", []))
    new_benefits_str = st.text_area("Каждое преимущество с новой строки", value=benefits_text, height=150)
    new_benefits = [b.strip() for b in new_benefits_str.split("\n") if b.strip()]
    
    # System Prompt
    st.subheader("Системный Промпт (Инструкция для ИИ)")
    new_prompt = st.text_area("Инструкция (Persona)", value=knowledge.get("system_prompt_template", ""), height=400)
    
    if st.button("Сохранить изменения"):
        knowledge["intro"] = new_intro
        knowledge["benefits"] = new_benefits
        knowledge["system_prompt_template"] = new_prompt
        
        save_knowledge(knowledge)
        st.success("База знаний обновлена! Бот подхватит изменения автоматически (при следующем сообщении).")
