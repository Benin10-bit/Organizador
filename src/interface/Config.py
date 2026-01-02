import customtkinter as ctk
from tkinter import filedialog

from organizador.blacklist import BlackList
from organizador.rules import Ruler

class Config(ctk.CTkFrame):
    def __init__(self, master):
        # Inicializa o frame principal com fundo preto
        super().__init__(master, fg_color="#000000")
        self.master = master

        self.blacklist = BlackList()

        # instancia o gerenciador de regras
        self.ruler = Ruler()
        self.rules = self.ruler.loadRules()  # lista atual de regras

        # ========================= ÁREA PRINCIPAL COM SCROLL =========================
        # Frame com scroll para todo o conteúdo principal
        scroll = ctk.CTkScrollableFrame(self, 
                                       fg_color="#000000", 
                                       corner_radius=0,
                                       scrollbar_button_color="#1a1a1a",
                                       scrollbar_button_hover_color="#2a2a2a")
        scroll.pack(side="left", fill="both", expand=True)

        # Container centralizado para todo o conteúdo
        content = ctk.CTkFrame(scroll, fg_color="transparent")
        content.pack(fill="both", expand=True, padx=40, pady=40)

        # ================================ CONFIGURAÇÕES ================================

        # --- input blacklist ---

        blacklistFrame = ctk.CTkFrame(content, 
                                   fg_color="#0a0a0a", 
                                   width=500,
                                   corner_radius=12, 
                                   border_width=1, 
                                   border_color="#1a1a1a")
        blacklistFrame.pack(fill="x", pady=30)

        blacklist_beforeinner = ctk.CTkFrame(blacklistFrame, fg_color="transparent")
        blacklist_beforeinner.pack(fill="x")

        blacklist_inner = ctk.CTkFrame(blacklistFrame, fg_color="transparent")
        blacklist_inner.pack(fill="x", padx=30, pady=25)


        blacklistLabel = ctk.CTkLabel(blacklist_beforeinner, 
                                      text= "Bloquear pastas",
                                      font=ctk.CTkFont(size=18, weight="bold"),
                                      text_color="#ffffff")
        blacklistLabel.pack(side="left",padx=30, pady=(20, 0))

        blacklist_row = ctk.CTkFrame(blacklist_inner, fg_color="transparent")
        blacklist_row.pack(fill="x")

        self.entrada_caminho = ctk.CTkEntry(blacklist_row,
                                           placeholder_text="Nenhuma pasta selecionada...",
                                           height=45,
                                           font=ctk.CTkFont(size=14),
                                           fg_color="#000000",
                                           border_color="#1a1a1a",
                                           state="disabled")  # Desabilitado para não editar manualmente
        self.entrada_caminho.pack(side="left", fill="x", expand=True, padx=(0, 10))

        # Botão para abrir o seletor de pasta
        btn_selecionar = ctk.CTkButton(blacklist_row,
                                      text="Selecionar Pasta",
                                      command=self.selecionar_pasta,
                                      width=180,
                                      height=45,
                                      font=ctk.CTkFont(size=14, weight="bold"),
                                      fg_color="#3b82f6",
                                      hover_color="#2563eb")
        btn_selecionar.pack(side="left")

        self.resultadoLabel = ctk.CTkLabel(blacklistFrame, text="")
        self.resultadoLabel.pack(pady=20, padx=30)

        #--- REGRAS ---
        rulesFrame = ctk.CTkFrame(content, 
                                   fg_color="#0a0a0a", 
                                   width=500,
                                   corner_radius=12, 
                                   border_width=1, 
                                   border_color="#1a1a1a")
        rulesFrame.pack(fill="x", pady=30)

        rules_inner = ctk.CTkFrame(rulesFrame, fg_color="transparent")
        rules_inner.pack(fill="x", padx=30, pady=20)

        # Header row
        header = ctk.CTkFrame(rules_inner, fg_color="transparent")
        header.pack(fill="x", pady=(0,8))
        ctk.CTkLabel(header, text="Tipo", width=120, anchor="w", text_color="#ffffff").pack(side="left")
        ctk.CTkLabel(header, text="Entrada Regra", anchor="w", text_color="#ffffff").pack(side="left", padx=(10,0), expand=True)
        ctk.CTkLabel(header, text="Destino", anchor="w", text_color="#ffffff", width=220).pack(side="left", padx=(10,0))
        ctk.CTkLabel(header, text="", width=160).pack(side="left")  # espaço para botões/status

        # Nota explicativa
        note = ctk.CTkLabel(rules_inner, text="Dica: use 'tam_min' em bytes ou com sufixos (KB, MB, GB). Salve para atualizar/registrar regras.", text_color="#9ca3af", anchor="w")
        note.pack(fill="x", pady=(0,8))

        # cria 3 linhas editáveis com design melhorado
        self.rule_rows = []
        for i in range(3):
            row = ctk.CTkFrame(rules_inner, fg_color="#070707", corner_radius=8, border_width=1, border_color="#1a1a1a")
            row.pack(fill="x", pady=6)

            tipo_menu = ctk.CTkOptionMenu(row, values=["contem", "ext", "tam_min"], width=120)
            tipo_menu.set("contem")
            tipo_menu.pack(side="left", padx=8, pady=8)

            entrada = ctk.CTkEntry(row, placeholder_text="texto / ext / tamanho", height=38, font=ctk.CTkFont(size=13))
            entrada.pack(side="left", padx=(6,0), expand=True, fill="x")

            destino = ctk.CTkEntry(row, placeholder_text="pasta destino", width=220, height=38, font=ctk.CTkFont(size=13))
            destino.pack(side="left", padx=(10,0), pady=8)

            # status badge (texto pequeno com cor)
            resultado = ctk.CTkLabel(row, text="", width=120, anchor="e")
            resultado.pack(side="left", padx=(10,6))

            # botões Salvar e Remover
            btn_frame = ctk.CTkFrame(row, fg_color="transparent")
            btn_frame.pack(side="left", padx=(0,10))
            btn_salvar = ctk.CTkButton(btn_frame, text="Salvar", width=90, height=34,
                                       command=lambda i=i, t=tipo_menu, e=entrada, d=destino, r=resultado: self.salvar_regra(i, t, e, d, r))
            btn_salvar.pack(side="left", padx=(0,6))
            btn_remover = ctk.CTkButton(btn_frame, text="Remover", width=80, height=34, fg_color="#ef4444",
                                        hover_color="#dc2626",
                                        command=lambda i=i, r=resultado: self.remover_regra(i, r))
            btn_remover.pack(side="left")

            # preenche com regra existente se houver
            existing_index = i if i < len(self.rules) else None
            if existing_index is not None:
                rule = self.rules[existing_index]
                # detecta tipo e valor
                if "contem" in rule:
                    tipo_menu.set("contem")
                    entrada.insert(0, str(rule.get("contem", "")))
                elif "ext" in rule:
                    tipo_menu.set("ext")
                    entrada.insert(0, str(rule.get("ext", "")))
                elif "tam_min" in rule:
                    tipo_menu.set("tam_min")
                    entrada.insert(0, str(rule.get("tam_min", "")))
                destino.insert(0, str(rule.get("move_to", "")))

            self.rule_rows.append({"widget": (tipo_menu, entrada, destino, resultado), "rule_index": existing_index})

        # Lista de regras atuais (visão geral)
        sep = ctk.CTkFrame(rules_inner, fg_color="transparent")
        sep.pack(fill="x", pady=(12,0))
        ctk.CTkLabel(sep, text="Regras Atuais:", font=ctk.CTkFont(size=15, weight="bold"), text_color="#ffffff").pack(anchor="w", padx=6)
        self.rules_list_frame = ctk.CTkScrollableFrame(rules_inner, fg_color="#0b0b0b", height=160)
        self.rules_list_frame.pack(fill="x", pady=(8,0), padx=(0,6))
        self.refresh_rules_list()

    def selecionar_pasta(self):
        """Abre o diálogo para selecionar uma pasta e atualiza a interface"""
        # Abre o file dialog para escolher uma pasta
        pasta = filedialog.askdirectory(title="Selecione a pasta para Bloquear")
        
        if pasta:  # Se o usuário selecionou algo
            self.caminho_selecionado = pasta
            # Habilita temporariamente o campo para atualizar o texto
            self.entrada_caminho.configure(state="normal")
            self.entrada_caminho.delete(0, "end")
            self.entrada_caminho.insert(0, pasta)
            self.entrada_caminho.configure(state="disabled")

            self.adicionarBlacklist(pasta)
    
    def adicionarBlacklist(self, pasta):
        res = self.blacklist.addToBlackList(pasta)
        self.resultadoLabel.configure(text=res if res else "Adicionado a blacklist com sucesso" , text_color="#10b981" if not res else "#ef4444")

    def parse_size(self, val_str):
        """Converte strings como '10MB', '5k' ou '1024' para bytes (int)."""
        s = val_str.strip().lower()
        if not s:
            return None
        # permite separador decimal com vírgula
        s = s.replace(",", ".")
        multipliers = {"k": 1024, "kb": 1024, "m": 1024**2, "mb": 1024**2, "g": 1024**3, "gb": 1024**3, "b": 1}
        # detecta sufixo
        for suf, mul in multipliers.items():
            if s.endswith(suf) and suf != "b":
                try:
                    num = float(s[: -len(suf)])
                    return int(num * mul)
                except Exception:
                    return None
        # sem sufixo: tenta inteiro
        try:
            return int(float(s))
        except Exception:
            return None

    def refresh_rules_list(self):
        """Atualiza a lista de regras exibidas (visão geral)."""
        # limpa frame
        for w in self.rules_list_frame.winfo_children():
            w.destroy()

        self.rules = self.ruler.loadRules() or []
        if not self.rules:
            ctk.CTkLabel(self.rules_list_frame, text="Nenhuma regra cadastrada.", text_color="#9ca3af").pack(anchor="w", padx=8, pady=6)
            return

        for idx, rule in enumerate(self.rules):
            line = ctk.CTkFrame(self.rules_list_frame, fg_color="transparent")
            line.pack(fill="x", padx=6, pady=4)
            desc = ""
            if "contem" in rule:
                desc = f"contem: '{rule.get('contem')}'"
            elif "ext" in rule:
                desc = f"ext: '{rule.get('ext')}'"
            elif "tam_min" in rule:
                desc = f"tam_min: {rule.get('tam_min')}"
            dest = rule.get("move_to", "")
            ctk.CTkLabel(line, text=f"{idx+1}. {desc}  →  {dest}", anchor="w", text_color="#e5e7eb").pack(side="left", expand=True, fill="x", padx=(4,0))
            btn_del = ctk.CTkButton(line, text="Excluir", width=90, fg_color="#ef4444", hover_color="#dc2626",
                                    command=lambda i=idx: self.force_remove_rule(i))
            btn_del.pack(side="right", padx=(0,6))

    def remover_regra(self, row_index, resultado_label):
        """Limpa os campos da linha e remove a regra correspondente se existir."""
        row_info = self.rule_rows[row_index]
        tipo_menu, entrada, destino, resultado = row_info["widget"]
        rule_idx = row_info.get("rule_index")
        # limpa campos da UI
        tipo_menu.set("contem")
        entrada.delete(0, "end")
        destino.delete(0, "end")
        resultado.configure(text="Linha limpa", text_color="#f59e0b")
        # se havia uma regra mapeada, remove do arquivo
        if rule_idx is not None and 0 <= rule_idx < len(self.rules):
            try:
                del self.rules[rule_idx]
                self.ruler.saveRules(self.rules)
                # atualiza mapeamentos: recarrega e recoloca índices
                self.refresh_rules_list()
                # atualiza mapeamento dos rows (simples: recarregar indices)
                self.reassign_row_indices()
                resultado.configure(text="Regra removida", text_color="#10b981")
            except Exception:
                resultado.configure(text="Erro ao remover", text_color="#ef4444")
        else:
            # apenas limpa e atualiza lista (caso tenha sido uma linha vazia)
            self.refresh_rules_list()

    def force_remove_rule(self, idx):
        """Remoção forçada pela lista de regras."""
        try:
            rules = self.ruler.loadRules() or []
            if 0 <= idx < len(rules):
                del rules[idx]
                self.ruler.saveRules(rules)
            self.refresh_rules_list()
            # reassign indices in editable rows
            self.reassign_row_indices()
        except Exception:
            pass

    def reassign_row_indices(self):
        """Reatribui rule_index aos rows a partir do arquivo (preenche até 3 primeiras regras)."""
        self.rules = self.ruler.loadRules() or []
        for i, row_info in enumerate(self.rule_rows):
            if i < len(self.rules):
                row_info["rule_index"] = i
                tipo_menu, entrada, destino, resultado = row_info["widget"]
                # atualiza visual com o valor atual da regra
                entrada.delete(0, "end")
                destino.delete(0, "end")
                rule = self.rules[i]
                if "contem" in rule:
                    tipo_menu.set("contem"); entrada.insert(0, str(rule.get("contem", "")))
                elif "ext" in rule:
                    tipo_menu.set("ext"); entrada.insert(0, str(rule.get("ext", "")))
                elif "tam_min" in rule:
                    tipo_menu.set("tam_min"); entrada.insert(0, str(rule.get("tam_min", "")))
                destino.insert(0, str(rule.get("move_to", "")))
            else:
                row_info["rule_index"] = None

    def salvar_regra(self, index, tipo_menu, entrada, destino, resultado_label):
        """Valida campos, cria a regra e salva no arquivo via Ruler (atualiza ou adiciona)."""
        tipo = tipo_menu.get()
        val = entrada.get().strip()
        move_to = destino.get().strip()

        if not val:
            resultado_label.configure(text="Entrada vazia", text_color="#ef4444")
            return
        if not move_to:
            resultado_label.configure(text="Destino vazio", text_color="#ef4444")
            return

        # converte tam_min para bytes se necessário
        rule_obj = {}
        if tipo == "tam_min":
            parsed = self.parse_size(val)
            if parsed is None:
                resultado_label.configure(text="tam_min inválido", text_color="#ef4444")
                return
            rule_obj["tam_min"] = parsed
        else:
            rule_obj[tipo] = val

        rule_obj["move_to"] = move_to

        try:
            rules = self.ruler.loadRules() or []
            # decide se atualiza uma regra existente vinculada à linha
            row_info = self.rule_rows[index]
            rule_idx = row_info.get("rule_index")
            if rule_idx is not None and 0 <= rule_idx < len(rules):
                rules[rule_idx] = rule_obj
                resultado_label.configure(text="Regra atualizada", text_color="#10b981")
            else:
                rules.append(rule_obj)
                # vincula esta linha ao último índice criado
                row_info["rule_index"] = len(rules) - 1
                resultado_label.configure(text="Regra adicionada", text_color="#10b981")

            self.ruler.saveRules(rules)
            # atualiza cache local e a lista visível
            self.rules = rules
            self.refresh_rules_list()
        except Exception:
            resultado_label.configure(text="Erro ao salvar", text_color="#ef4444")