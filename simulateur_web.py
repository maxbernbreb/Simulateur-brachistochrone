import streamlit as st
import streamlit.components.v1 as components    
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# streamlit run simulateur_web.py

# 1. CONFIGURATION DE LA PAGE
st.set_page_config(page_title="Simulateur Brachistochrone", layout="wide")
st.title("Simulateur de Trajectoires : Brachistochrone")

# 2. PANNEAU DE CONTRÔLE (Sidebar)
st.sidebar.header("Paramètres de la cible")

xm = st.sidebar.slider("Position X d'arrivée (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)
ym = st.sidebar.slider("Profondeur Y d'arrivée (m)", min_value=5.0, max_value=50.0, value=10.0, step=0.5)

st.sidebar.markdown("---")
st.sidebar.subheader("Courbes à afficher")
afficher_brachi = st.sidebar.checkbox("Brachistochrone (Cycloïde)", value=True)
afficher_droite = st.sidebar.checkbox("Ligne Droite", value=True)
afficher_para = st.sidebar.checkbox("Parabole", value=True)
afficher_log = st.sidebar.checkbox("Logarithme", value=True)

g = 9.81
N = 1000

# 3. CALCULS MATHÉMATIQUES 
t = 5
#Calcul courbe Brachi
for _ in range(1000): t=t - ((t-np.sin(t))/(1-np.cos(t))-xm/ym)/(np.sin(t)*(np.sin(t)-t)/(1-np.cos(t))**2+1) #newton
r=ym/(1-np.cos(t))
 
#Calculs de temps
subdivs=1000000
print("Calcul integral")
b=ym**2/xm
interx1, interx2 = np.array([i*xm/subdivs for i in range(1,subdivs)]),  np.array([i*xm/subdivs for i in range(2,subdivs+1)])
intery1, intery2 = np.array([i*ym/subdivs for i in range(1,subdivs)]),  np.array([i*ym/subdivs for i in range(2,subdivs+1)])
m=ym/xm**0.5
temps_parabole =ym/(subdivs*3*m**2*(2*g)**0.5)*sum([2*(1+(i+1)%2)*(m**4/intery1[i]+4*intery1[i])**0.5 for i in range(0,subdivs-1)],(m**4/ym+4*ym)**0.5)
m= (np.exp(ym)-1)/xm

temps_logarithme = ym/(subdivs*3*(2*g)**0.5)*sum([2*(1+(i+1)%2)*(((np.exp(intery1[i])/m)**2+1)/intery1[i])**0.5 for i in range(0,subdivs-1)],((1/(m*np.exp(ym))**2+1)/ym)**0.5)

temps_droite = (xm**2+ym**2)**0.5*(2/(g*ym))**0.5

temps_cycloide=(r/g)**0.5*t

# 4. CRÉATION DU GRAPHIQUE
plt.style.use('dark_background')
fig, ax = plt.subplots(figsize=(10, 5))

fig.patch.set_alpha(0.0)
ax.patch.set_alpha(0.0)
# On inverse l'axe Y pour que ça ressemble à une chute
ax.invert_yaxis() 
ax.set_xlabel("Distance X (m)")
ax.set_ylabel("Profondeur Y (m)")

# On dessine le point de départ et d'arrivée
ax.plot([0], [0])
ax.plot([xm], [ym])

# 5. AFFICHAGE CONDITIONNEL
if afficher_brachi:
    list_t = np.array(range(N+1))/N * t
    list_x_brachi = r * (list_t - np.sin(list_t))
    list_y_brachi = r * (1 - np.cos(list_t))
    ax.plot(list_x_brachi, list_y_brachi, label="Brachistochrone", color='red', linewidth=2)

if afficher_droite:
    liste_droite = np.array(range(N+1))/N * xm
    liste_y_droite = (ym/xm) * liste_droite
    ax.plot(liste_droite, liste_y_droite, label='Droite', color='blue', linewidth=2)

if afficher_para:
    liste_para_x = np.array(range(N+1))/N * xm
    liste_y_para = (liste_para_x**0.5) * ym / (xm**0.5)
    ax.plot(liste_para_x, liste_y_para, label='Parabole', color='green', linewidth=2)

if afficher_log:
    liste_log_x = np.array(range(N+1))/N * xm
    m_log = (np.exp(ym) - 1) / xm
    liste_log_y = np.log(m_log * liste_log_x + 1)
    ax.plot(liste_log_x, liste_log_y, label='Logarithme', color='orange', linewidth=2)

ax.legend()

# 6. ENVOI DU GRAPHIQUE SUR LA PAGE WEB
col1, col2 = st.columns([3, 1])

with col1:
    st.pyplot(fig)

with col2:
    st.subheader("Temps estimés")
    st.info(f" **Brachistochrone:** {temps_cycloide:.3f} s")
    st.info(f" **Ligne Droite:** {temps_droite:.3f} s")
    st.info(f" **Parabole:** {temps_parabole:.3f} s")
    st.info(f" **Logarithme:** {temps_logarithme:.3f} s")

st.markdown("---")
st.subheader("Course en temps réel")

if st.button("Lancer l'animation physique"):
    
    with st.spinner("Génération de l'animation..."):
        
        FPS = 30
        dt_affichage = 1/FPS
        ani_temps, ani_brachi_x, ani_brachi_y = [], [], []
        ani_droite_x, ani_droite_y = [], []
        ani_para_x, ani_para_y = [], []
        ani_log_x, ani_log_y = [], [] 

        fig_ani, ax_ani = plt.subplots(figsize=(10, 5))
        
        ax_ani.set_xlim(-1, xm + 1)
        ax_ani.set_ylim(-ym - 1, 1) 
        
        # Trace les lignes de fond (pistes). 
        if afficher_brachi: ax_ani.plot(list_x_brachi, -list_y_brachi, 'r-', linewidth=1)
        if afficher_droite: ax_ani.plot(liste_droite, -liste_y_droite, 'b-', linewidth=1)
        if afficher_para: ax_ani.plot(liste_para_x, -liste_y_para, 'g-', linewidth=1)
        if afficher_log: ax_ani.plot(liste_log_x, -liste_log_y,color = 'orange', linewidth=1)
        # Billes vides
        point_brachi, = ax_ani.plot([], [], 'ro', markersize=8)
        point_droite, = ax_ani.plot([], [], 'bo', markersize=8)
        point_para, = ax_ani.plot([], [], 'go', markersize=8)
        point_log, = ax_ani.plot([], [], 'o', color='orange', markersize=8)
        time_text = ax_ani.text(0.80, 0.90, '', transform=ax_ani.transAxes, fontsize=12)

        # 3. CALCUL PHYSIQUE
        x_brachi=y_brachi=x_droite=y_droite=x_para=y_para=x_log=y_log = 0.000000000000000001
        N_sim = 10000 
        dx = px = lgx = 0.000000000000001
        dt = 1/FPS/N_sim
        m_log = xm/(np.exp(ym)-1)
        temps = 0
        next_frame_time = 0
     
        while x_droite <= xm or x_para <= xm or x_log <= xm:
            if temps >= next_frame_time:
                ani_temps.append(temps)
                ani_brachi_x.append(min(x_brachi, xm))
                ani_brachi_y.append(y_brachi if x_brachi < xm else -ym)
                ani_droite_x.append(min(x_droite, xm))
                ani_droite_y.append(y_droite if x_droite < xm else -ym)
                ani_para_x.append(min(x_para, xm))
                ani_para_y.append(y_para if x_para < xm else -ym)
                ani_log_x.append(min(x_log, xm))
                ani_log_y.append(y_log if x_log < xm else -ym)
                next_frame_time += dt_affichage
            temps += dt
            
            if x_brachi < xm:
                t_b = temps/((r/g)**0.5) 
                x_brachi = r*(t_b-np.sin(t_b))
                y_brachi = -r*(1-np.cos(t_b))
            
            if x_droite < xm:
                x_droite += dx * xm / (xm**2+ym**2)**0.5
                y_droite -= dx * ym / (xm**2+ym**2)**0.5
                dx = (2*g*-y_droite)**0.5 * dt
     
            if x_para < xm:
                x_para += px / ((ym/(xm**0.5*x_para**0.5*2))**2+1)**0.5
                y_para -= px * (ym/(xm**0.5*x_para**0.5*2)) / ((ym/(xm**0.5*x_para**0.5*2))**2+1)**0.5
                px = (2*g*-y_para)**0.5 * dt
     
            if x_log < xm:
                x_log += lgx * (x_log+m_log) / (((x_log+m_log)**2+1)**0.5)
                y_log -= lgx / (((x_log+m_log)**2+1)**0.5)
                lgx = (2*g*-y_log)**0.5 * dt

        # 4. CRÉATION DU GIF
        def update(frame):
            if afficher_brachi: point_brachi.set_data([ani_brachi_x[frame]], [ani_brachi_y[frame]])
            if afficher_droite: point_droite.set_data([ani_droite_x[frame]], [ani_droite_y[frame]])
            if afficher_para: point_para.set_data([ani_para_x[frame]], [ani_para_y[frame]])
            if afficher_log: point_log.set_data([ani_log_x[frame]], [ani_log_y[frame]])
            time_text.set_text(f'Temps = {ani_temps[frame]:.2f} s')
            return point_brachi, point_droite, point_para, point_log, time_text

        from matplotlib.animation import FuncAnimation
        ani = FuncAnimation(fig_ani, update, frames=len(ani_temps), interval=1000/FPS, blit=True)
        
        fichier_temporaire = "course_temp.gif"
        ani.save(fichier_temporaire, writer='pillow', fps=FPS)
        
        st.image(fichier_temporaire, use_container_width=True)
        st.success("Course terminée !")

# Ai vs Brachi
st.markdown("---")
st.header("Duel Final : Brachistochrone vs Intelligence Artificielle")
st.write("Cette section compare la courbe mathématique parfaite et le résultat de notre IA après des millions de simulations.")


@st.cache_data
def generer_lecteur_duel():
    # Cibles
    x_duel = 5 * np.pi 
    y_duel = 10.0      
    t_duel = 5.0
    
    # Équation Newton
    t_newton = t_duel
    for _ in range(10): 
        t_newton = t_newton - ((t_newton-np.sin(t_newton))/(1-np.cos(t_newton))-x_duel/y_duel)/(np.sin(t_newton)*(np.sin(t_newton)-t_newton)/(1-np.cos(t_newton))**2+1)
    r_duel = y_duel / (1 - np.cos(t_newton))

    # Chargement IA
    ia_x_phys = np.load("ia_meilleure_courbe_X.npy")
    ia_y_brut = np.load("ia_meilleure_courbe_Y.npy")
    ia_y_affichage = y_duel - ia_y_brut # Inversion pour affichage correct
    
    # Calculs temps
    list_t_duel = np.array(range(N+1))/N * t_newton
    list_x_brachi_duel = r_duel * (list_t_duel - np.sin(list_t_duel))
    list_y_brachi_duel = r_duel * (1 - np.cos(list_t_duel))
    temps_cycloide_duel = (r_duel/g)**0.5 * t_newton
    
    temps_ia = 0
    v = 0
    ia_t_tot = [0]
    for i in range(len(ia_x_phys) - 1):
        dx = ia_x_phys[i+1] - ia_x_phys[i]
        dy = ia_y_affichage[i+1] - ia_y_affichage[i]
        dist = (dx**2 + dy**2)**0.5
        v_suivante = (2 * g * abs(ia_y_affichage[i+1]))**0.5
        v_moyenne = (v + v_suivante) / 2
        if v_moyenne > 0:
            temps_ia += dist / v_moyenne
        v = v_suivante
        ia_t_tot.append(temps_ia)

    # Paramètres d'animation
    temps_max_sim = max(temps_cycloide_duel, temps_ia) * 1.1 
    FPS = 60 
    frames_totales = int(temps_max_sim * FPS)
    temps_simule = np.linspace(0, temps_max_sim, frames_totales)
    
    ani_theorie_x, ani_theorie_y = [], []
    ani_ia_x, ani_ia_y = [], []
    
    for t_actuel in temps_simule:
        pct = min(1.0, t_actuel / temps_cycloide_duel)
        idx = int(pct * (len(list_x_brachi_duel) - 1))
        ani_theorie_x.append(list_x_brachi_duel[idx])
        ani_theorie_y.append(list_y_brachi_duel[idx])
        
        if t_actuel >= temps_ia:
            ani_ia_x.append(ia_x_phys[-1])
            ani_ia_y.append(ia_y_affichage[-1])
        else:
            ani_ia_x.append(np.interp(t_actuel, ia_t_tot, ia_x_phys))
            ani_ia_y.append(np.interp(t_actuel, ia_t_tot, ia_y_affichage))

    fig_anim, ax_anim = plt.subplots(figsize=(10, 5))
    fig_anim.patch.set_alpha(0.0) # Fond image transparent
    ax_anim.patch.set_alpha(0.0)  # Fond graphique transparent
    ax_anim.invert_yaxis()
    ax_anim.set_xlim(-1, x_duel + 1)
    ax_anim.set_ylim(y_duel + 1, -1)
    ax_anim.set_xlabel("Distance X (m)")
    ax_anim.set_ylabel("Profondeur Y (m)")

    couler_brachi = '#5EC9CC' 
    couler_ia = '#ED7943F4'
    
    ax_anim.plot(list_x_brachi_duel, list_y_brachi_duel,color = couler_brachi, linewidth=2, label="Brachistochrone")
    ax_anim.plot(ia_x_phys, ia_y_affichage, color = couler_ia, linewidth=2, label="IA")
    
    point_brachi_duel, = ax_anim.plot([], [], color = couler_brachi, marker='o', markersize=8)
    point_ia_duel, = ax_anim.plot([], [], color = couler_ia, marker='o', markersize=8)
    time_text_duel = ax_anim.text(0.05, 0.9, '', transform=ax_anim.transAxes, fontsize=12, color='white')
    ax_anim.legend(loc="upper right")

    def update_duel(frame):
        point_brachi_duel.set_data([ani_theorie_x[frame]], [ani_theorie_y[frame]])
        point_ia_duel.set_data([ani_ia_x[frame]], [ani_ia_y[frame]])
        time_text_duel.set_text(f'Chronomètre : {temps_simule[frame]:.2f} s')
        return point_brachi_duel, point_ia_duel, time_text_duel

    ani_duel = FuncAnimation(fig_anim, update_duel, frames=frames_totales, interval=1000/FPS, blit=False)
    html_code = ani_duel.to_jshtml()
    plt.close(fig_anim) 
    
    return html_code, temps_cycloide_duel, temps_ia

try:
    html_anim_pret, temps_cycloide_final, temps_ia_final = generer_lecteur_duel()
    
    # Affichage des scores
    col_score1, col_score2 = st.columns(2)
    col_score1.success(f"**Temps théorique absolu :** {temps_cycloide_final:.5f} s")
    col_score2.info(f"**Temps IA (20 pts) :** {temps_ia_final:.5f} s")
    
    # Affichage direct du lecteur, sans bouton !
    components.html(html_anim_pret, height=600)

except FileNotFoundError:
    st.warning("Les fichiers du cerveau de l'IA (.npy) sont introuvables dans ce dossier.")