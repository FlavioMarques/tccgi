import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image

# Security
# passlib,hashlib,bcrypt,scrypt

import hashlib

bg_color = st.get_option("theme.backgroundColor")
grid_color = "#ABB8C3"

def make_hashes(password):
	return hashlib.sha256(str.encode(password)).hexdigest()
def check_hashes(password,hashed_text):
	if make_hashes(password) == hashed_text:
		return hashed_text
	return False

# DB Management
import sqlite3 
conn = sqlite3.connect('data.db')
c = conn.cursor()
# DB  Functions
def create_usertable():
	c.execute('CREATE TABLE IF NOT EXISTS userstable(username TEXT,password TEXT)')

def add_userdata(username,password):
	c.execute('INSERT INTO userstable(username,password) VALUES (?,?)',(username,password))
	conn.commit()

def login_user(username,password):
	c.execute('SELECT * FROM userstable WHERE username =? AND password = ?',(username,password))
	data = c.fetchall()
	return data

def view_all_users():
	c.execute('SELECT * FROM userstable')
	data = c.fetchall()
	return data


def main(bg_color=grid_color):
	image = Image.open('logotipo.png')

	ccol1, ccol2, ccol3 = st.columns(3)

	with ccol2:
		st.image(image, caption='Projeto TCC FactoryFlow')

		"""**** Faça Login no App ****"""

	st.title("Factory Flow")

	menu = ["Inicio","Login","Assinatura"]
	choice = st.sidebar.selectbox("Menu",menu)

	if choice == "Inicio":
		st.subheader("Inicio")
		st.write("""
		Bem-vindo ao painel de produção FactoryFlow. Nosso design simples, mas profissional, ajuda você a entender os KPIs mais importantes do seu processo de produção.
		Com esta ferramenta você pode facilmente analisar a eficiência de sua fábrica, identificar gargalos e otimizar seus processos. FactoryFlow foca na criação
		de painéis para empresas de manufatura. O mercado desses painéis tem crescido fortemente nos últimos anos, pois as empresas buscam soluções para tornar seus processos produtivos mais eficientes
		e torná-lo mais eficaz. Os concorrentes nesse mercado geralmente oferecem soluções semelhantes, como monitoramento em tempo real, análise preditiva e ferramentas de comunicação integradas.
		Alguns players bem conhecidos neste mercado são Siemens, GE Digital e ABB. \t

		O FactoryFlow se diferencia da concorrência concentrando-se em fornecer painéis personalizados fáceis de usar e fáceis de implementar.
		Isso torna mais fácil para as empresas de manufatura otimizar rapidamente seus processos e ver resultados imediatos. \t

		Vamos aumentar a produtividade juntos!
		""")


	elif choice == "Login":
		st.subheader("Login na Seção")

		username = st.sidebar.text_input("Nome")
		password = st.sidebar.text_input("Senha",type='password')
		if st.sidebar.checkbox("Entrar"):
			# if password == '12345':
			create_usertable()
			hashed_pswd = make_hashes(password)

			result = login_user(username,check_hashes(password,hashed_pswd))
			if result:

				st.success("Logado como {}".format(username))

				task = st.selectbox("Tarefas",["Produção","Analises","Cadastro"])
				if task == "Produção":
					st.subheader("Adicionar serviços setores/maquinas")

				elif task == "Analises":
					st.subheader("Monitoramento de produção")

					st.header("Estatísticas rápidas")
					col1, col2 = st.columns(2)

					with col1:
						st.subheader("Volume de produção")
						st.write("1234")

					with col2:
						st.subheader("Número de máquinas ativas")
						st.write("18")

					col3, col4 = st.columns(2)

					with col3:
						st.subheader("Pedidos em aberto")
						st.write("150")

					with col4:
						st.subheader("Volume de negócios total")
						st.write("R$ 200.000")

					# Grafieken onder elkaar
					st.header("Gráficos")

					# Tweede grafiek: Oorzaak uitvaltijd (Piechart)
					st.header("Causa do tempo de inatividade")
					oorzaken = ["Máquina quebrada", "Partes faltando", "Manutenção", "Mau funcionamento desconhecido"]
					percentages = [30, 20, 40, 10]

					plt.figure(figsize=(7, 4))
					sns.set_palette("pastel")
					plt.pie(percentages, autopct="%1.1f%%", startangle=90)
					plt.legend(oorzaken, title="Causas", loc="best")
					plt.axis("equal")

					plt.gca().set_facecolor(bg_color)
					plt.gca().set_axis_off()

					st.pyplot(plt.gcf())

					# Derde grafiek: Top 5 verkochte producten
					st.subheader("5 produtos mais vendidos")
					product_data = pd.DataFrame({
						"Produto": ["Botijão 2KG", "Botijão 13KG", "Botijão 45KG"],
						"Preço": [100, 200, 350],
						"Quantidade vendida": [50, 30, 20],
						"Receita": [5000, 6000, 7000]
					})

					# Verberg indexkolom bij het weergeven van het DataFrame
					st.write(product_data.to_html(index=False, border=0, classes=["table", "table-striped"]),
							 unsafe_allow_html=True)

					# Vierde grafiek: Teruggestuurde producten (Stacked bar graph)
					st.header("Produtos devolvidos")
					terugstuur_oorzaken = ["Quebrado", "Diferente do esperado", "Sem motivo"]
					terugstuur_data = pd.DataFrame({
						"Produto": ["Botijão 2KG", "Botijão 13KG", "Botijão 45KG"],
						"Quebrado": [10, 15, 20],
						"Diferente do esperado": [5, 8, 10],
						"Sem motivo": [7, 10, 15]
					})

					fig, ax = plt.subplots(figsize=(7, 4))
					sns.set_palette("deep")
					terugstuur_data.set_index("Produto")[terugstuur_oorzaken].plot(kind="bar", stacked=True, ax=ax)
					ax.set_ylabel("Número de produtos devolvidos")
					ax.set_title("Produtos devolvidos por causa")

					bg_color = "white"
					ax.set_facecolor(bg_color)
					plt.gca().spines["top"].set_visible(False)
					plt.gca().spines["right"].set_visible(False)
					plt.gca().spines["bottom"].set_color(grid_color)
					plt.gca().spines["left"].set_color(grid_color)

					st.pyplot(fig)

				elif task == "Cadastro":
					st.subheader("Usuarios Registrados")
					user_result = view_all_users()
					clean_db = pd.DataFrame(user_result,columns=["Username","Password"])
					st.dataframe(clean_db)
			else:
				st.warning("Incorreto Usuario/Senha")





	elif choice == "Assinatura":
		st.subheader("Criar Nova Conta")
		new_user = st.text_input("Usuario")
		new_password = st.text_input("Senha",type='password')

		if st.button("Assinatura"):
			create_usertable()
			add_userdata(new_user,make_hashes(new_password))
			st.success("Você criou com sucesso uma conta válida")
			st.info("Vá para o menu Login para fazer o login")


if __name__ == '__main__':
	main()