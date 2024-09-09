import tkinter as tk
from tkinter import messagebox, filedialog
import psycopg2
import csv

# Função para conectar ao banco de dados PostgreSQL
def connect_db():
    try:
        conexao = psycopg2.connect(
            dbname="isp_clients", user="postgres", password="Acesso01", host="localhost", port="5432"
        )
        return conexao
    except Exception as e:
        messagebox.showerror("Erro de Conexão", f"Não foi possível conectar ao banco de dados: {e}")
        return None

# Validação para garantir que o campo ID aceite apenas números inteiros
def validate_int(value_if_allowed):
    if value_if_allowed.isdigit() or value_if_allowed == "":
        return True
    else:
        return False

# Função para inserir um novo cliente
def insert_cliente():
    conexao = connect_db()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute(
                "INSERT INTO clientes (nome_empresa, responsavel, telefone, cidade_estado, asn, operadora_principal, ipv4, ipv6, dominio) "
                "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                (
                    entry_nome_empresa.get(),
                    entry_responsavel.get(),
                    entry_telefone.get(),
                    entry_cidade_estado.get(),
                    entry_asn.get(),
                    entry_operadora.get(),
                    entry_ipv4.get(),
                    entry_ipv6.get(),
                    entry_dominio.get(),
                ),
            )
            conexao.commit()
            messagebox.showinfo("Sucesso", "Cliente inserido com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir cliente: {e}")
        finally:
            conexao.close()

# Função para excluir um cliente por ID
def delete_cliente():
    cliente_id = entry_id_cliente.get()
    if not cliente_id:
        messagebox.showwarning("Aviso", "Por favor, informe o ID do cliente para exclusão.")
        return

    conexao = connect_db()
    if conexao:
        try:
            cursor = conexao.cursor()
            cursor.execute("DELETE FROM clientes WHERE id = %s", (cliente_id,))
            if cursor.rowcount == 0:
                messagebox.showinfo("Info", "Nenhum cliente encontrado com o ID fornecido.")
            else:
                conexao.commit()
                messagebox.showinfo("Sucesso", "Cliente excluído com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao excluir cliente: {e}")
        finally:
            conexao.close()

# Função para consultar clientes com filtros adicionais
def query_clientes():
    conexao = connect_db()
    if conexao:
        try:
            cursor = conexao.cursor()
            
            # Construção da query dinâmica com filtros
            query = "SELECT * FROM clientes WHERE TRUE"
            params = []
            
            if entry_nome_empresa_filter.get():
                query += " AND nome_empresa = %s"
                params.append(entry_nome_empresa_filter.get())
            
            if entry_cidade_estado_filter.get():
                query += " AND cidade_estado = %s"
                params.append(entry_cidade_estado_filter.get())
                
            cursor.execute(query, params)
            results = cursor.fetchall()
            
            # Exibe os resultados na área de texto
            resultado_text.delete('1.0', tk.END)
            if results:
                for row in results:
                    resultado_text.insert(tk.END, f"ID: {row[0]}, Nome: {row[1]}, Responsável: {row[2]}, Telefone: {row[3]}, Cidade/Estado: {row[4]}, ASN: {row[5]}\n")
            else:
                resultado_text.insert(tk.END, "Nenhum cliente encontrado com os filtros aplicados.")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro na consulta: {e}")
        finally:
            conexao.close()

# Função para selecionar arquivo CSV e fazer inserção em massa
def insert_bulk_from_csv():
    file_path = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
    if not file_path:
        return

    conexao = connect_db()
    if conexao:
        try:
            cursor = conexao.cursor()
            with open(file_path, newline='', encoding='utf-8') as csvfile:
                reader = csv.reader(csvfile, delimiter=',')
                next(reader)  # Pula o cabeçalho do CSV
                for row in reader:
                    cursor.execute(
                        "INSERT INTO clientes (nome_empresa, responsavel, telefone, cidade_estado, asn, operadora_principal, ipv4, ipv6, dominio) "
                        "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)",
                        row
                    )
            conexao.commit()
            messagebox.showinfo("Sucesso", "Clientes inseridos em massa com sucesso!")
        except Exception as e:
            messagebox.showerror("Erro", f"Erro ao inserir clientes em massa: {e}")
        finally:
            conexao.close()

# Configuração da janela principal do Tkinter
root = tk.Tk()
root.title("Gerenciamento de Clientes ISP")

# Título da seção de inserção de dados
tk.Label(root, text="Inserção de Dados", font=('Helvetica', 14, 'bold')).grid(row=0, column=0, columnspan=2, pady=10)

# Campos de entrada para inserção de dados
tk.Label(root, text="Nome da Empresa:").grid(row=1, column=0, padx=10, pady=5)
entry_nome_empresa = tk.Entry(root)
entry_nome_empresa.grid(row=1, column=1, padx=10, pady=5)

tk.Label(root, text="Responsável:").grid(row=2, column=0, padx=10, pady=5)
entry_responsavel = tk.Entry(root)
entry_responsavel.grid(row=2, column=1, padx=10, pady=5)

tk.Label(root, text="Telefone:").grid(row=3, column=0, padx=10, pady=5)
entry_telefone = tk.Entry(root)
entry_telefone.grid(row=3, column=1, padx=10, pady=5)

tk.Label(root, text="Cidade/Estado:").grid(row=4, column=0, padx=10, pady=5)
entry_cidade_estado = tk.Entry(root)
entry_cidade_estado.grid(row=4, column=1, padx=10, pady=5)

tk.Label(root, text="ASN:").grid(row=5, column=0, padx=10, pady=5)
entry_asn = tk.Entry(root)
entry_asn.grid(row=5, column=1, padx=10, pady=5)

tk.Label(root, text="Operadora Principal:").grid(row=6, column=0, padx=10, pady=5)
entry_operadora = tk.Entry(root)
entry_operadora.grid(row=6, column=1, padx=10, pady=5)

tk.Label(root, text="IPv4:").grid(row=7, column=0, padx=10, pady=5)
entry_ipv4 = tk.Entry(root)
entry_ipv4.grid(row=7, column=1, padx=10, pady=5)

tk.Label(root, text="IPv6:").grid(row=8, column=0, padx=10, pady=5)
entry_ipv6 = tk.Entry(root)
entry_ipv6.grid(row=8, column=1, padx=10, pady=5)

tk.Label(root, text="Domínio:").grid(row=9, column=0, padx=10, pady=5)
entry_dominio = tk.Entry(root)
entry_dominio.grid(row=9, column=1, padx=10, pady=5)

# Título da seção de filtros e exclusão
tk.Label(root, text="Filtros e Exclusão", font=('Helvetica', 14, 'bold')).grid(row=0, column=2, columnspan=2, pady=10)

# Campos de entrada para filtros
tk.Label(root, text="Filtro Nome da Empresa:").grid(row=1, column=2, padx=10, pady=5)
entry_nome_empresa_filter = tk.Entry(root)
entry_nome_empresa_filter.grid(row=1, column=3, padx=10, pady=5)

tk.Label(root, text="Filtro Cidade/Estado:").grid(row=2, column=2, padx=10, pady=5)
entry_cidade_estado_filter = tk.Entry(root)
entry_cidade_estado_filter.grid(row=2, column=3, padx=10, pady=5)

# Campo de entrada para ID do cliente para exclusão
tk.Label(root, text="ID do Cliente para Exclusão:").grid(row=3, column=2, padx=10, pady=5)
entry_id_cliente = tk.Entry(root, validate="key", validatecommand=(root.register(validate_int), "%P"))
entry_id_cliente.grid(row=3, column=3, padx=10, pady=5)

# Botões de ações
tk.Button(root, text="Inserir Cliente", command=insert_cliente).grid(row=10, column=0, padx=10, pady=10)
tk.Button(root, text="Excluir Cliente", command=delete_cliente).grid(row=10, column=1, padx=10, pady=10)
tk.Button(root, text="Consultar Cliente", command=query_clientes).grid(row=10, column=2, padx=10, pady=10)
tk.Button(root, text="Inserir em Massa (CSV)", command=insert_bulk_from_csv).grid(row=10, column=3, padx=10, pady=10)

# Área de exibição dos resultados
resultado_text = tk.Text(root, height=10, width=100)
resultado_text.grid(row=11, column=0, columnspan=4, padx=10, pady=10)

root.mainloop()