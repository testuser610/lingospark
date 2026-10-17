import random
from datetime import datetime
import streamlit as st

st.set_page_config(page_title="LingoSpark", page_icon="✨", layout="wide")
st.markdown("""<style>
.stApp{background:linear-gradient(180deg,#f2f7ff,#fffdf6)}
h1,h2,h3{color:#163a70}
div[data-testid="stMetric"]{background:white;border:1px solid #d9e6ff;border-radius:15px;padding:12px}
.card{background:white;border:1px solid #d9e6ff;border-radius:16px;padding:16px;margin:6px 0}
.badge{display:inline-block;background:#edf4ff;border:1px solid #cbdcff;border-radius:30px;padding:5px 10px;margin:3px}
</style>""", unsafe_allow_html=True)

COURSES = {
"Everyday English":[
("Greetings",[("Hello","ഹലോ"),("Good morning","സുപ്രഭാതം"),("How are you?","സുഖമാണോ?")],"What does Good morning mean?",["സുപ്രഭാതം","ശുഭ രാത്രി","നന്ദി"],"സുപ്രഭാതം"),
("At the shop",[("How much is this?","ഇതിന് എത്രയാണ്?"),("I would like this","എനിക്ക് ഇത് വേണം"),("Thank you","നന്ദി")],"Choose a polite phrase.",["Give me now","Thank you","Go away"],"Thank you")],
"Vocabulary":[
("Food words",[("Apple","ആപ്പിൾ"),("Rice","അരി"),("Water","വെള്ളം")],"Which word means വെള്ളം?",["Water","Rice","Apple"],"Water"),
("Places",[("Hospital","ആശുപത്രി"),("Library","ലൈബ്രറി"),("Market","ചന്ത")],"Where can you borrow books?",["Market","Library","Hospital"],"Library")],
"Grammar":[
("I am / You are",[("I am happy","ഞാൻ സന്തോഷവാനാണ്"),("You are kind","നിങ്ങൾ ദയയുള്ളവരാണ്"),("She is here","അവൾ ഇവിടെയുണ്ട്")],"You ___ my friend.",["am","is","are"],"are"),
("Simple questions",[("What is your name?","നിങ്ങളുടെ പേരെന്താണ്?"),("Where are you from?","നിങ്ങൾ എവിടെ നിന്നാണ്?"),("How old are you?","നിങ്ങൾക്ക് എത്ര വയസ്സുണ്ട്?")],"Which is a question?",["I am fine.","Where are you from?","She is happy."],"Where are you from?")],
"Listening practice":[("Listen and choose",[("Please","ദയവായി"),("Listen","കേൾക്കുക"),("Repeat","ആവർത്തിക്കുക")],"What does Please mean?",["ദയവായി","വേഗം","വിട"],"ദയവായി")],
"Speaking practice":[("Say it aloud",[("My name is…","എന്റെ പേര്…"),("I am learning English","ഞാൻ ഇംഗ്ലീഷ് പഠിക്കുകയാണ്"),("Nice to meet you","കണ്ടുമുട്ടിയതിൽ സന്തോഷം")],"Which phrase introduces your name?",["My name is…","Good night","See you later"],"My name is…")]
}
BADGES = [
("🌱","First Sprout","Complete your first lesson",lambda s:s["lessons"]>=1),
("📖","Page Turner","Complete 10 lessons",lambda s:s["lessons"]>=10),
("🧠","Word Wizard","Study 100 words",lambda s:s["words"]>=100),
("🎧","Sound Seeker","Complete 20 listening practices",lambda s:s["listening"]>=20),
("🔥","Flame Keeper","Reach a 7-day streak",lambda s:s["streak"]>=7),
("⚡","Momentum Master","Complete 5 lessons",lambda s:s["lessons"]>=5),
("✨","Spark Starter","Earn 100 XP",lambda s:s["xp"]>=100),
("🚀","Rocket Riser","Earn 1,000 XP",lambda s:s["xp"]>=1000),
("💎","Crystal Climber","Earn 5,000 XP",lambda s:s["xp"]>=5000),
("⏱️","Time Tamer","Win 5 challenges",lambda s:s["wins"]>=5),
("🤝","Friendly Spark","Follow a learner",lambda s:len(s["following"])>=1),
("🧰","Treasure Tracker","Open 10 chests",lambda s:s["chests"]>=10),
("🧢","Style Collector","Collect 5 accessories",lambda s:len(s["items"])>=5),
("🎯","Precision Pro","Get 10 quiz answers right",lambda s:s["correct"]>=10),
("🗝️","Secret Finder","Discover a secret badge",lambda s:s["secret"]),
]
DEMO = [("FinnixFan23",2450,12,7),("GrammarHero",1980,10,12),("MimiLearner",1760,8,5),("TikoMaster",1540,7,3),("PogoPal",920,6,9)]

defaults={"username":"Learner","xp":0,"coins":0,"lessons":0,"words":0,"correct":0,"total":0,"streak":1,"hearts":5,
"following":[],"earned":[],"chests":0,"items":["Blue Star Hoodie"],"listening":0,"speaking":0,"wins":0,
"minutes":0,"goal":15,"mistakes":[],"activity":[],"secret":False}
for k,v in defaults.items():
    if k not in st.session_state: st.session_state[k]=v

def activity(msg):
    st.session_state.activity.insert(0,datetime.now().strftime("%H:%M")+" — "+msg)
    st.session_state.activity=st.session_state.activity[:12]
def award(xp,why):
    st.session_state.xp+=xp; st.session_state.coins+=max(1,xp//10); activity(f"+{xp} XP: {why}"); check_badges()
def check_badges():
    for icon,name,desc,condition in BADGES:
        if condition(st.session_state) and name not in st.session_state.earned:
            st.session_state.earned.append(name); activity("🏆 Unlocked: "+name)

with st.sidebar:
    st.markdown("# ✨ LingoSpark")
    st.caption("Learn • Practice • Grow")
    page=st.radio("Menu",["🏠 Home","📚 Learn","🧩 Quiz & Practice","🏆 Achievements","👥 Friends","⚔️ Leagues","🎁 Rewards","👤 Profile","⚙️ Settings"])
    st.divider()
    st.markdown(f"**🦊 {st.session_state.username}**")
    st.progress((st.session_state.xp%1000)/1000,text=f"Level {st.session_state.xp//1000+1}")
    st.caption(f"🔥 {st.session_state.streak}-day streak · ❤️ {st.session_state.hearts}")

if page=="🏠 Home":
    st.title(f"Hello, {st.session_state.username}! 👋")
    st.subheader("Ready for a little learning adventure?")
    cols=st.columns(4)
    for col,label,val in zip(cols,["⭐ XP","🪙 Coins","🔥 Streak","📚 Lessons"],[st.session_state.xp,st.session_state.coins,f'{st.session_state.streak} days',st.session_state.lessons]):
        col.metric(label,val)
    st.markdown('<div class="card"><h3>🦊 Finnix says hello!</h3>Small steps make big progress. Complete a lesson, collect XP, and unlock a badge today.</div>',unsafe_allow_html=True)
    st.write(f"### 🎯 Daily goal — {st.session_state.minutes}/{st.session_state.goal} minutes")
    st.progress(min(st.session_state.minutes/max(st.session_state.goal,1),1))
    if st.session_state.minutes>=st.session_state.goal: st.success("Daily goal complete!")
    st.subheader("Recent activity")
    st.write("\n".join("• "+x for x in st.session_state.activity[:6]) if st.session_state.activity else "Your activity will appear here.")

elif page=="📚 Learn":
    st.title("📚 Learning Path")
    course=st.selectbox("Choose a course",list(COURSES))
    lessons=COURSES[course]
    title=st.selectbox("Choose a lesson",[x[0] for x in lessons])
    lesson=next(x for x in lessons if x[0]==title)
    st.subheader("🦊 "+title)
    st.write("Study the English words and Malayalam meanings.")
    st.table([{"English":a,"Malayalam":b} for a,b in lesson[1]])
    st.markdown("### Quick check")
    answer=st.radio(lesson[2],lesson[3],key=f"lesson_{course}_{title}")
    if st.button("Check lesson answer",type="primary"):
        if answer==lesson[4]:
            st.success("Correct! Well done! 🎉")
            st.session_state.lessons+=1; st.session_state.words+=len(lesson[1]); st.session_state.minutes+=3
            if course=="Listening practice": st.session_state.listening+=1
            if course=="Speaking practice": st.session_state.speaking+=1
            award(25,"completed "+title); st.rerun()
        else:
            st.error("Not quite. Review the words and try again.")
            st.session_state.hearts=max(0,st.session_state.hearts-1)
            st.session_state.mistakes.append((lesson[2],answer,lesson[4]))
    st.caption("Speaking and listening are text-based demos; real speech/audio features need extra services.")

elif page=="🧩 Quiz & Practice":
    st.title("🧩 Practice Zone")
    t1,t2,t3=st.tabs(["Daily quiz","Challenge","Mistake review"])
    with t1:
        pool=[x for group in COURSES.values() for x in group]
        q=random.choice(pool)
        st.write(q[2]); ans=st.radio("Choose an answer",q[3],key="daily_answer")
        if st.button("Submit quiz"):
            st.session_state.total+=1
            if ans==q[4]:
                st.session_state.correct+=1; award(15,"daily quiz"); st.success("Correct! +15 XP")
            else:
                st.session_state.mistakes.append((q[2],ans,q[4])); st.error("Correct answer: "+q[4])
            st.rerun()
        if st.session_state.total: st.caption(f"Accuracy: {round(st.session_state.correct/st.session_state.total*100)}%")
    with t2:
        st.write("Try a challenge to earn extra XP.")
        if st.button("Start challenge"): st.session_state.challenge=random.choice([("Complete: I ___ happy.","are",["am","is","are"]),("What does Apple mean?","ആപ്പിൾ",["ആപ്പിൾ","വെള്ളം","അരി"]),("Choose a greeting.","Hello",["Hello","Never","Away"])])
        if "challenge" in st.session_state:
            q=st.session_state.challenge; ans=st.radio(q[0],q[2],key="challenge_ans")
            if st.button("Finish challenge"):
                if ans==q[1]:
                    st.session_state.wins+=1; award(30,"challenge won"); st.success("You won! +30 XP")
                else: st.error("Correct answer: "+q[1])
                del st.session_state.challenge; st.rerun()
    with t3:
        if not st.session_state.mistakes: st.info("No mistakes saved yet.")
        for i,(q,a,c) in enumerate(st.session_state.mistakes,1): st.write(f"{i}. **{q}** · Your answer: {a} · Correct: **{c}**")
        if st.session_state.mistakes and st.button("Clear reviewed mistakes"): st.session_state.mistakes=[]; st.rerun()

elif page=="🏆 Achievements":
    st.title("🏆 Achievement Hall")
    st.metric("Badges unlocked",f"{len(st.session_state.earned)} / {len(BADGES)}")
    for row in range(0,len(BADGES),3):
        cols=st.columns(3)
        for col,(icon,name,desc,condition) in zip(cols,BADGES[row:row+3]):
            unlocked=name in st.session_state.earned
            with col:
                st.markdown(f'<div class="card"><h1>{icon if unlocked else "🔒"}</h1><b>{name}</b><p>{desc}</p><span class="badge">{"UNLOCKED" if unlocked else "LOCKED"}</span></div>',unsafe_allow_html=True)

elif page=="👥 Friends":
    st.title("👥 Friends & Following")
    st.write("Search learners, follow them, and cheer for their progress.")
    search=st.text_input("Search username")
    for name,xp,level,streak in DEMO:
        if search.lower() not in name.lower(): continue
        with st.container(border=True):
            a,b,c=st.columns([2,2,1])
            a.markdown(f"### 🧑‍🎓 {name}"); a.caption(f"Level {level} · 🔥 {streak}-day streak")
            b.write(f"⭐ {xp} XP")
            if name in st.session_state.following:
                if c.button("Following ✓",key="un_"+name): st.session_state.following.remove(name); activity("Unfollowed "+name); st.rerun()
            else:
                if c.button("＋ Follow",key="fo_"+name): st.session_state.following.append(name); activity("Followed "+name); check_badges(); st.rerun()
    st.subheader(f"Following ({len(st.session_state.following)})")
    st.write(", ".join(st.session_state.following) or "Follow a learner to get started.")
    st.subheader("Activity from followed learners")
    for name,xp,level,streak in DEMO:
        if name in st.session_state.following:
            st.info(f"{name} has {xp} XP and is continuing their learning journey.")
            if st.button("👏 Congratulate "+name,key="cheer_"+name): award(2,"sent a cheer"); st.success("Cheer sent in this demo!")
    st.caption("Demo profiles only. Real cross-device social features require secure accounts and a database.")

elif page=="⚔️ Leagues":
    st.title("⚔️ League Arena")
    rows=[(name,xp) for name,xp,_,_ in DEMO]+[(st.session_state.username,st.session_state.xp)]
    rows.sort(key=lambda x:x[1],reverse=True)
    st.table([{"Rank":i+1,"Learner":n,"XP":xp} for i,(n,xp) in enumerate(rows)])
    xp=st.session_state.xp
    league="Bronze" if xp<500 else "Silver" if xp<1500 else "Gold" if xp<3500 else "Platinum" if xp<7000 else "Diamond"
    st.success("Your demo league: "+league)
    st.caption("Other players and scores are sample data.")

elif page=="🎁 Rewards":
    st.title("🎁 Rewards Shop")
    st.metric("🪙 Coins",st.session_state.coins)
    shop=[("⭐ Star Pin",30),("🧢 Explorer Cap",60),("🕶️ Cool Glasses",80),("🧣 Winter Scarf",100),("🌈 Rainbow Theme",120)]
    for name,cost in shop:
        a,b=st.columns([3,1]); a.write(f"**{name}** · {cost} coins")
        if name in st.session_state.items: b.button("Owned ✓",disabled=True,key="owned_"+name)
        elif b.button("Unlock",key="buy_"+name):
            if st.session_state.coins>=cost:
                st.session_state.coins-=cost; st.session_state.items.append(name); activity("Unlocked "+name); check_badges(); st.rerun()
            else: st.error("Earn more coins by completing lessons.")
    st.subheader("Mystery chest")
    if st.button("Open chest — 100 coins"):
        if st.session_state.coins>=100:
            st.session_state.coins-=100; st.session_state.chests+=1; prize=random.choice([10,20,30,50]); st.session_state.coins+=prize
            award(5,"opened a chest"); st.success(f"You found {prize} bonus coins and 5 XP!"); st.rerun()
        else: st.warning("You need 100 coins.")

elif page=="👤 Profile":
    st.title("👤 Learner Profile")
    st.subheader("🦊 "+st.session_state.username)
    a,b,c=st.columns(3); a.metric("Level",st.session_state.xp//1000+1); b.metric("XP",st.session_state.xp); c.metric("Following",len(st.session_state.following))
    st.subheader("Your badges")
    st.write(" · ".join(st.session_state.earned) or "Complete a lesson to earn your first badge.")
    st.subheader("Unlocked items"); st.write(", ".join(st.session_state.items))
    st.subheader("Learning statistics")
    st.write(f"Lessons: {st.session_state.lessons} · Words studied: {st.session_state.words}")
    st.write(f"Quiz accuracy: {round(st.session_state.correct/max(st.session_state.total,1)*100)}%")
    st.write(f"Speaking practices: {st.session_state.speaking} · Listening practices: {st.session_state.listening}")

elif page=="⚙️ Settings":
    st.title("⚙️ Settings")
    st.session_state.username=st.text_input("Display name",st.session_state.username,max_chars=24)
    st.session_state.goal=st.slider("Daily goal (minutes)",5,60,st.session_state.goal,5)
    st.toggle("Private profile (demo setting)",key="private_profile")
    st.toggle("Sound effects (demo setting)",key="sound_effects")
    st.caption("Settings are temporary in this prototype.")
    if st.button("Add 100 demo XP"): award(100,"demo bonus"); st.rerun()
    if st.button("Unlock secret achievement"):
        st.session_state.secret=True; check_badges(); st.success("Secret badge discovered!"); st.rerun()
    if st.button("Reset progress"):
        for k,v in defaults.items(): st.session_state[k]=v.copy() if isinstance(v,list) else v
        st.rerun()

st.divider()
st.caption("LingoSpark • Learn • Practice • Grow | Prototype demo — not yet a production app")
