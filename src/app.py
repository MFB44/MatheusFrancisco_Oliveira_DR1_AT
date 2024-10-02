import streamlit as st
from statsbombpy import sb
from mplsoccer import Pitch, Sbopen
import matplotlib.pyplot as plt
import time

parser = Sbopen()
@st.cache_data
def match_data(match_id):
    return parser.event(match_id)[0]

st.set_page_config(page_title='Assessment Soccer', page_icon='⚽', layout='centered', initial_sidebar_state='auto')

menu = ['Introdução', 'Análise Total', 'Pergunta']
choice = st.sidebar.selectbox('Menu', menu)
colormap = {   
    'Black': '#000000',
    'White': '#FFFFFF',
    'Gray': '#808080',     
    'Red': '#FF0000',
    'Blue': '#0000FF',
    'Green': '#00FF00',
    'Yellow': '#FFFF00',
    'Orange': '#FFA500',
    'Purple': '#800080',
    'Pink': '#FFC0CB',
    'Brown': '#A52A2A',
    'Navy': '#000080',
    'Cyan': '#00FFFF',
    'Magenta': '#FF00FF',
    'Gold': '#FFD700',
    'Silver': '#C0C0C0',
}
st.markdown(f'''
<style>
.stApp {{
    background-color: {colormap[st.sidebar.selectbox('Escolha uma cor para o background:', list(colormap.keys()))]};
}}
</style>
''', unsafe_allow_html=True)

if choice == 'Introdução':
    st.markdown("<h1 style='text-align: center;'>Assessment - Desenvolvimento Front-End com Python (com Streamlit)</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='text-align: center;'>Matheus Francisco - Ciência de Dados INFNET</h3>", unsafe_allow_html=True)
    st.image('https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExZjFiaHlyMGN3aHY5YnJnajMwcDNrY2hlM2Fmb3Izam5leXdxd3RnNiZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9dg/RNlgWpfnRNRGBES99r/giphy.gif', use_column_width=True)
    st.markdown("<p style='text-align: center;'>Nesta aplicação você encontra três páginas. Esta, uma introdução ao projeto com todos os detalhes necessários; A 'análise total' dos dados contidos na biblioteca Statsbombpy, onde você pode filtrar e analisar da forma que preferir; e a 'pergunta', que corresponde ao enunciado do Assessment, que solicitava uma pergunta a ser respondida.</p>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center;'>A questão respondida neste Assessment é 'Quantos gols uma equipe marcou durante toda a duração de uma Copa do Mundo?'. Neste caso, você poderá escolher, dentre as equipes presentes na base, qualquer time participante de qualquer Copa do Mundo, desde a Copa de 1958. Escolhendo qual Copa você quer analisar, é possível visualizar e escolher qual time visualizar. Com isso é disponibilizado a data de cada partida a qual a equipe marcou um gol, e um mapa com todos os chutes feitos em dada partida, mostrando de onde foi marcado cada gol. Também é informado qual jogadaor e em qual minuto tal gol foi marcado. E claro, contra qual outra equipe esta partida se refere.</p>", unsafe_allow_html=True)
    st.markdown("<h5 style='text-align: center; color: cyan;'>Aproveite a aplicação e divirta-se!</h5>", unsafe_allow_html=True)

elif choice == 'Análise Total':
    st.title('Complete Analysis')

    competitions = sb.competitions()
    competitions_names = competitions['competition_name'].unique()
    choose_competition = st.selectbox('Choose a competition', competitions_names)

    with st.spinner('Loading...'):
        time.sleep(10)
        st.dataframe(competitions[competitions['competition_name'] == choose_competition])
        csv_competition = competitions[competitions['competition_name'] == choose_competition].to_csv(index=False)
        st.download_button(
            label="Download Competition Data as CSV",
            data=csv_competition,
            file_name='competition_data.csv',
            mime='text/csv',
        )

    competition_id = competitions[competitions['competition_name'] == choose_competition]['competition_id'].values[0]
    if 'competition_id' not in st.session_state:
        st.session_state['competition_id'] = competition_id

    seasons = competitions[competitions['competition_name'] == choose_competition]['season_name'].unique()
    season_name = st.selectbox('Choose a season', seasons)
    season_id = competitions[competitions['season_name'] == season_name]["season_id"].values[0]
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    if 'competitions' not in st.session_state:
        st.session_state['competitions'] = competitions
    if 'matches' not in st.session_state:
        st.session_state['matches'] = matches
    if 'season_name' not in st.session_state:
        st.session_state['season_name'] = season_name
    if 'season_id' not in st.session_state:
        st.session_state['season_id'] = season_id

    @st.cache_data
    def get_match_label(match_id):
        row = matches[matches['match_id'] == match_id].iloc[0]
        
        return f"{row['match_date']} : {row['home_team']} vs {row['away_team']}"

    game = st.selectbox('Choose a match', matches['match_id'], format_func=get_match_label)

    with st.spinner('Loading...'):
        time.sleep(10)
        with st.container():
            st.title("Details")
            date = matches[matches['match_id'] == game]['match_date'].values[0]
            st.markdown(f"<h2 style='text-align: center; color: orange;'>{date}</h2>", unsafe_allow_html=True)
            try:
                referee = matches[matches['match_id'] == game]['referee'].values[0]
                st.markdown(f"<h6 style='text-align: center; color: green;'>Referee:</h6>", unsafe_allow_html=True)
                st.markdown(f"<h6 style='text-align: center; color: green;'>{referee}</h6>", unsafe_allow_html=True)
            except:
                st.markdown(f"<h6 style='text-align: center; color: green;'>No referee information</h6>", unsafe_allow_html=True)

    with st.expander("All Match Passes and Shots"):
        st.write("All passes from the match")
        passes = sb.events(match_id=game, split=True, flatten_attrs=False)["passes"]
        st.dataframe(passes)
        csv = passes.to_csv(index=False)
        st.download_button(
            label="Download Passes as CSV",
            data=csv,
            file_name='passes.csv',
            mime='text/csv',
        )

        st.write("All shots from the match")
        shots = sb.events(match_id=game, split=True, flatten_attrs=False)["shots"]
        st.dataframe(shots)
        csv = shots.to_csv(index=False)
        st.download_button(
            label="Download Shots as CSV",
            data=csv,
            file_name='shots.csv',
            mime='text/csv',
        )

    left_column, right_column = st.columns(2)
    with st.container():
        with left_column:
            st.write("Home Team")
            home_team = matches[matches['match_id'] == game]['home_team'].values[0]
            st.subheader(home_team)
            home_score = matches[matches['match_id'] == game]['home_score'].values[0]
            st.metric("Goals", home_score)
                    
        with right_column:
            st.write("Away Team")
            away_team = matches[matches['match_id'] == game]['away_team'].values[0]
            st.subheader(away_team)
            away_score = matches[matches['match_id'] == game]['away_score'].values[0]
            st.metric("Goals", away_score)

    line_ups = sb.lineups(match_id=game)
    data = match_data(game)

    st.cache_data
    def plot_passes(match, player):
        player_filter = (match.type_name == 'Pass') & (match.player_name == player)
        df_pass = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y']]
        pitch = Pitch(pitch_color='grass', line_color='black', stripe=True)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
        pitch.kdeplot(df_pass.x, df_pass.y, ax=ax['pitch'], alpha=0.5, shade=True, cmap='inferno')
        return fig

    @st.cache_data
    def plot_kicks(match, player):
        player_filter = (match.type_name == 'Shot') & (match.player_name == player)
        df_kick = match.loc[player_filter, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]
        pitch = Pitch(pitch_color='grass', line_color='black', stripe=True)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
        
        goals = df_kick[df_kick['outcome_name'] == 'Goal']
        pitch.arrows(goals.x, goals.y, goals.end_x, goals.end_y, ax=ax['pitch'], color='yellow', label='Goal')
        
        misses = df_kick[df_kick['outcome_name'] != 'Goal']
        pitch.arrows(misses.x, misses.y, misses.end_x, misses.end_y, ax=ax['pitch'], color='red', label='Miss')
        
        ax['pitch'].legend(loc='upper right', fontsize=20)

        return fig
    
    @st.cache_data
    def plot_pie_chart(match, player):
        player_data = match[(match.player_name == player)]
        total_passes = player_data[player_data.type_name == 'Pass'].shape[0]
        total_shots = player_data[player_data.type_name == 'Shot'].shape[0]
        goals = player_data[(player_data.type_name == 'Shot') & (player_data.outcome_name == 'Goal')].shape[0]
        missed_shots = total_shots - goals

        labels = ['Passes', 'Goals', 'Missed Shots']
        sizes = [total_passes, goals, missed_shots]
        colors = ['#011e8a','#d1e561','#942a2a']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%',
               shadow=True, startangle=140)
        ax.axis('equal')

        return fig

    st.markdown("<h3 style='text-align: center;'>Heatmap of Passes and Shots Map by Player</h3>", unsafe_allow_html=True)
    col_1, col_2 = st.columns(2)

    with col_1:
        player_h = st.selectbox('Player', line_ups[home_team]['player_name'])
        with st.spinner('Loading...'):
            time.sleep(10)
            fig_1 = plot_passes(data, player_h)
            fig_2 = plot_kicks(data, player_h)
            st.write('Passes')
            st.pyplot(fig_1)
            st.write('Shots')
            st.pyplot(fig_2)
            fig_6 = plot_pie_chart(data, player_h)
            st.pyplot(fig_6)

    with col_2:
        player_a = st.selectbox('Player', line_ups[away_team]['player_name'])
        with st.spinner('Loading...'):
            time.sleep(10)
            fig_4 = plot_passes(data, player_a)
            fig_5 = plot_kicks(data, player_a)
            st.write('Passes')
            st.pyplot(fig_4)
            st.write('Shots')
            st.pyplot(fig_5)
            fig_7 = plot_pie_chart(data, player_a)
            st.pyplot(fig_7)

else:
    st.title('Quantos Gols cada equipe marcou durante cada Copa do Mundo?')

    competitions = sb.competitions()
    world_cup = competitions[(competitions['competition_name'] == 'FIFA World Cup')]
    competition_id = world_cup['competition_id'].values[0]
    seasons = competitions[competitions['competition_name'] == 'FIFA World Cup']['season_name'].unique()
    season_name = st.selectbox('Choose a season', seasons)
    season_id = competitions[competitions['season_name'] == season_name]["season_id"].values[0]
    matches = sb.matches(competition_id=competition_id, season_id=season_id)
    if 'competitions' not in st.session_state:
        st.session_state['competitions'] = competitions
    if 'world_cup' not in st.session_state:
        st.session_state['world_cup'] = world_cup
    if 'competition_id' not in st.session_state:
        st.session_state['competition_id'] = competition_id
    if 'matches' not in st.session_state:
        st.session_state['matches'] = matches    
    if 'season_name' not in st.session_state:
        st.session_state['season_name'] = season_name
    if 'season_id' not in st.session_state:
        st.session_state['season_id'] = season_id

    teams = matches['home_team'].unique().tolist() + matches['away_team'].unique().tolist()
    teams = list(set(teams))
    teams.sort()

    with st.expander(f"Teams that participated in the {season_name} FIFA World Cup:"):
        st.write(teams)

    with st.container(border=True):
        team = st.selectbox('Choose a team', teams)

        def get_value(selected_option):
            time.sleep(6)
            if selected_option == team:
                return selected_option
            else:
                return None
            
        with st.spinner('Loading data...'):
            value = get_value(team)
            st.markdown(f"<h5 style='text-align: center; color: brown;'>Selected team: {value}</h5>", unsafe_allow_html=True)
    
    team_matches = matches[(matches['home_team'] == team) | (matches['away_team'] == team)]
    team_goals = team_matches[team_matches['home_team'] == team]['home_score'].sum() + team_matches[team_matches['away_team'] == team]['away_score'].sum()
    team_goal_matches = team_matches[(team_matches['home_team'] == team) & (team_matches['home_score'] > 0) | (team_matches['away_team'] == team) & (team_matches['away_score'] > 0)]
    if 'team_goal_matches' not in st.session_state:
        st.session_state['team_goal_matches'] = team_goal_matches
    if 'team_goals' not in st.session_state:
        st.session_state['team_goals'] = team_goals

    st.markdown(f"<h4 style='text-align: left; color: gold;'>Matches where {team} scored goals:</h4>", unsafe_allow_html=True)

    for index, match in team_goal_matches.iterrows():
        if match['home_team'] == team:
            opponent = match['away_team']
            goals = match['home_score']
        else:
            opponent = match['home_team']
            goals = match['away_score']
        
        st.write(f"Date: {match['match_date']}, Opponent: {opponent}, Goals: {goals}")

    st.markdown("<h3 style='text-align: center; color: green;'>Shots Map per Match</h3>", unsafe_allow_html=True)
    goal_scorers = []

    def plot_kicks(match, team):
        team_filter = (match.type_name == 'Shot') & (match.team_name == team)
        df_kick = match.loc[team_filter, ['x', 'y', 'end_x', 'end_y', 'outcome_name']]
        pitch = Pitch(pitch_color='grass', line_color='black', stripe=True)
        fig, ax = pitch.grid(grid_height=0.9, title_height=0.06, axis=False, endnote_height=0.04, title_space=0, endnote_space=0)
        
        goals = df_kick[df_kick['outcome_name'] == 'Goal']
        pitch.arrows(goals.x, goals.y, goals.end_x, goals.end_y, ax=ax['pitch'], color='yellow', label='Goal', headwidth=10, headlength=5)
        
        misses = df_kick[df_kick['outcome_name'] != 'Goal']
        pitch.arrows(misses.x, misses.y, misses.end_x, misses.end_y, ax=ax['pitch'], color='red', label='Miss', headwidth=2, headlength=2)

        pitch.arrows(misses.x, misses.y, misses.end_x, misses.end_y, ax=ax['pitch'], color='red', label='Miss', headwidth=2, headlength=2)
        
        ax['pitch'].legend(loc='upper right')
        return fig

    for index, match in team_goal_matches.iterrows():
        match_id = match['match_id']
        data = match_data(match_id)
        shots = data[data['type_name'] == 'Shot']
        team_shots = shots[shots['team_name'] == team]
        
        if match['home_team'] == team:
            opponent = match['away_team']
        else:
            opponent = match['home_team']
        
        st.markdown(f"### Match Date: {match['match_date']}, Opponent: {opponent}")
        
        for _, shot in team_shots.iterrows():
            if shot['outcome_name'] == 'Goal':
                goal_scorers.append(shot['player_name'])
                st.write(f"Goal scored by: {shot['player_name']} at minute {shot['minute']}")
        
        if not team_shots.empty:
            fig = plot_kicks(data, team)
            st.pyplot(fig)
    
    st.markdown(f"#### Players who scored goals for {team}:")
    p_goals = [{', '.join(set(goal_scorers))}]
    for p in p_goals:
        st.write(p)

    with st.container(border=True):
        st.markdown(f"<h3 style='text-align: center; color: green;'>{team} scored {team_goals} goals in the {season_name} FIFA World Cup!</h3>", unsafe_allow_html=True)