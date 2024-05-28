import json
import customtkinter
from screeninfo import get_monitors
from CTkMessagebox import CTkMessagebox as messagebox
from web3 import Web3
from decimal import Decimal

from graphic_elements_presets import *
from blockchain.client import Clients
from security import Security


class Application:
    clients: Clients

    def __init__(self):
        self.app = customtkinter.CTk()
        customtkinter.set_appearance_mode("Dark")
        self.app.title("Cryptocurrency Wallet")

        monitor = get_monitors()[0]
        self.app.geometry(f"{monitor.width // 4}x{monitor.height // 2}")

        with open('security_config.json') as f:
            wallet = json.load(f)['private_key'] != ''

        if not wallet:
            self.show_login_with_wallet_data()
        else:
            self.show_login_with_password()
            pass

    def show_login_with_password(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=0)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Enter Password", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.password_entry = customtkinter.CTkEntry(self.app, placeholder_text="Password", show="*")
        self.password_entry.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.login_button = customtkinter.CTkButton(
            self.app, text="Login", command=self.login_with_password, **default_button
        )
        self.login_button.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.reset_button = customtkinter.CTkButton(
            self.app, text="Reset wallet", command=self.reset_wallet, **default_back
        )
        self.reset_button.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=4, column=0)

    def show_login_with_wallet_data(self):
        for widget in self.app.winfo_children():
            widget.destroy()
        # Конфигурация сетки
        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)

        # Заголовок
        self.title_label = customtkinter.CTkLabel(self.app, text="Welcome to Your Wallet!", font=("Century Gothic", 30))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        # Кнопка для входа по приватному ключу
        self.private_key_button = customtkinter.CTkButton(
            self.app, text="Login with Private Key", command=self.show_private_key_login, **default_button
        )
        self.private_key_button.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        # Кнопка для входа по мнемонической фразе
        self.mnemonic_phrase_button = customtkinter.CTkButton(
            self.app, text="Login with Mnemonic Phrase", command=self.show_mnemonic_phrase_login, **default_button
        )
        self.mnemonic_phrase_button.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        # Заполнитель для нижнего отступа
        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=3, column=0, pady=(5, 10))

    def show_private_key_login(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)
        self.app.grid_rowconfigure(5, weight=0)
        self.app.grid_rowconfigure(6, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Enter Private Key", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.private_key_entry = customtkinter.CTkEntry(self.app, placeholder_text="Private Key")
        self.private_key_entry.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.password_entry = customtkinter.CTkEntry(self.app, placeholder_text="Create new password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.confirm_password_entry = customtkinter.CTkEntry(self.app, placeholder_text="Confirm password", show="*")
        self.confirm_password_entry.grid(row=3, column=0, padx=20, pady=(5, 50), sticky="ew")

        self.login_button = customtkinter.CTkButton(
            self.app, text="Login", command=self.login_with_private_key, **default_button
        )
        self.login_button.grid(row=4, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.back_button = customtkinter.CTkButton(
            self.app, text="Back", command=self.show_login_with_wallet_data, **default_back
        )
        self.back_button.grid(row=5, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=6, column=0)

    def show_mnemonic_phrase_login(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)
        self.app.grid_rowconfigure(5, weight=0)
        self.app.grid_rowconfigure(6, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Enter Mnemonic Phrase", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.mnemonic_phrase_entry = customtkinter.CTkEntry(self.app, placeholder_text="Mnemonic Phrase")
        self.mnemonic_phrase_entry.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.password_entry = customtkinter.CTkEntry(self.app, placeholder_text="Create new password", show="*")
        self.password_entry.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.confirm_password_entry = customtkinter.CTkEntry(self.app, placeholder_text="Confirm password", show="*")
        self.confirm_password_entry.grid(row=3, column=0, padx=20, pady=(5, 50), sticky="ew")

        self.login_button = customtkinter.CTkButton(
            self.app, text="Login", command=self.login_with_mnemonic_phrase, **default_button
        )
        self.login_button.grid(row=4, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.back_button = customtkinter.CTkButton(
            self.app, text="Back", command=self.show_login_with_wallet_data, **default_back
        )
        self.back_button.grid(row=5, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=6, column=0)

    def login_with_private_key(self):
        private_key = self.private_key_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not Clients.private_key_is_correct(private_key=private_key):
            messagebox(title="Error", message="Private key is incorrect!", icon="warning")
            return

        if password != confirm_password or len(password) < 1:
            messagebox(title="Error", message="Passwords do not match!", icon="warning")
            return

        self.clients = Clients(private_key=private_key)
        Security.set_password(password=password)
        Security.set_private_key(private_key=self.clients.private_key, password=password)
        self.show_assets()

    def login_with_mnemonic_phrase(self):
        mnemonic_phrase = self.mnemonic_phrase_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()

        if not Clients.mnemonic_phrase_is_correct(mnemonic_phrase=mnemonic_phrase):
            messagebox(title="Error", message="Mnemonic phrase is incorrect!", icon="warning")
            return

        if password != confirm_password or len(password) < 1:
            messagebox(title="Error", message="Passwords do not match!", icon="warning")
            return

        self.clients = Clients(mnemonic_phrase=mnemonic_phrase)
        Security.set_password(password=password)
        Security.set_private_key(private_key=self.clients.private_key, password=password)
        self.show_assets()

    def login_with_password(self):
        password = self.password_entry.get()
        if not Security.compare_password(password=password):
            messagebox(title="Error", message="Incorrect password!", icon="warning")
            return
        self.clients = Clients(private_key=Security.get_private_key(password=password))
        self.show_assets()

    def reset_wallet(self):
        Security.reset_data()
        self.show_login_with_wallet_data()

    def show_assets(self, default_network="Etherium"):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=1)
        self.app.grid_rowconfigure(0, weight=0)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=1)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)
        self.app.grid_rowconfigure(5, weight=0)
        self.app.grid_rowconfigure(5, weight=0)

        self.networks = self.clients.get_networks_names()
        self.tokens = self.clients.get_networks_with_tokens_list()

        # Combobox для выбора сети
        self.network_combobox = customtkinter.CTkComboBox(
            self.app, values=self.networks, command=self.update_tokens
        )
        self.network_combobox.grid(row=0, columnspan=2, padx=20, pady=(20, 10), sticky="ew")

        # Кнопка "Добавить сеть"
        self.add_network_button = customtkinter.CTkButton(
            self.app, text="Add network", command=self.show_add_network, **default_button
        )
        self.add_network_button.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        # Кнопка "Добавить токен"
        self.add_token_button = customtkinter.CTkButton(
            self.app, text="Add token", command=self.show_add_token, **default_button
        )
        self.add_token_button.grid(row=1, column=1, padx=20, pady=(5, 5), sticky="ew")

        # Список токенов
        self.tokens_listbox = customtkinter.CTkScrollableFrame(self.app)
        self.tokens_listbox.grid(row=2, columnspan=2, padx=20, pady=(10, 10), sticky="nsew")

        self.update_tokens(default_network)

        # Кнопка "Обновить баланс"
        self.update_balance_button = customtkinter.CTkButton(
            self.app, text="Update balance", command=self.update_tokens, **default_button
        )
        self.update_balance_button.grid(row=3, columnspan=2, padx=20, pady=(10, 5), sticky="ew")

        # Кнопка "Отправить транзакцию"
        self.send_transaction_button = customtkinter.CTkButton(
            self.app, text="Send transaction", command=self.show_sign_transaction, **default_button
        )
        self.send_transaction_button.grid(row=4, columnspan=2, padx=20, pady=(5, 5), sticky="ew")

        # Кнопка "Заблокировать кошелек"
        self.lock_wallet_button = customtkinter.CTkButton(
            self.app, text="Lock wallet", command=self.show_login_with_password, **default_back
        )
        self.lock_wallet_button.grid(row=5, columnspan=2, padx=20, pady=(20, 5), sticky="ew")

        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=6, column=0)

    def update_tokens(self, network: str | None = None):
        for widget in self.tokens_listbox.winfo_children():
            widget.destroy()
        if network:
            selected_network = network
            self.network_combobox.set(network)
        else:
            selected_network = self.network_combobox.get()
        tokens = self.tokens[selected_network]

        for token in tokens:
            token_label = customtkinter.CTkLabel(self.tokens_listbox,
                                                 text=f"{token}: {self.clients.get_balance(network_name=selected_network, token_name=token)}")
            token_label.pack(padx=10, pady=5, anchor="w")

    def show_add_network(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=0)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Add New Network", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.network_name_entry = customtkinter.CTkEntry(self.app, placeholder_text="Network Name")
        self.network_name_entry.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.network_rpc_entry = customtkinter.CTkEntry(self.app, placeholder_text="Network HTTP RPC")
        self.network_rpc_entry.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.add_network_button = customtkinter.CTkButton(
            self.app, text="Add Network", command=self.add_network, **default_button
        )
        self.add_network_button.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.back_button = customtkinter.CTkButton(
            self.app, text="Back", command=self.show_assets, **default_back
        )
        self.back_button.grid(row=4, column=0, padx=20, pady=(5, 20), sticky="ew")

    def add_network(self):
        network_name = self.network_name_entry.get().strip()
        network_rpc = self.network_rpc_entry.get().strip()

        if network_name and network_rpc:
            self.clients.add_network(network_name=network_name, rpc=network_rpc)
            self.tokens[network_name] = self.clients.clients_dict[network_name].network.tokens[
                self.clients.clients_dict[network_name].network.native_coin_symbol]
            self.show_assets(network_name)
        else:
            messagebox(title="Error", message="Both fields are required!", icon="warning")

    def show_add_token(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=0)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)
        self.app.grid_rowconfigure(5, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Add New Token", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.token_name_entry = customtkinter.CTkEntry(self.app, placeholder_text="Token Name")
        self.token_name_entry.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.token_contract_address_entry = customtkinter.CTkEntry(self.app, placeholder_text="Token Contract Address")
        self.token_contract_address_entry.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.network_combobox = customtkinter.CTkComboBox(
            self.app, values=self.networks
        )
        self.network_combobox.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.add_token_button = customtkinter.CTkButton(
            self.app, text="Add Token", command=self.add_token, **default_button
        )
        self.add_token_button.grid(row=4, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.back_button = customtkinter.CTkButton(
            self.app, text="Back", command=self.show_assets, **default_back
        )
        self.back_button.grid(row=5, column=0, padx=20, pady=(5, 20), sticky="ew")

    def add_token(self):
        token_name = self.token_name_entry.get().strip()
        token_contract_address = self.token_contract_address_entry.get().strip()
        network_name = self.network_combobox.get().strip()

        if token_name and token_contract_address and network_name:
            self.clients.clients_dict[network_name].network.add_token(token_name=token_name,
                                                                      contract_address=token_contract_address)
            self.show_assets(network_name)
        else:
            messagebox(title="Error", message="All fields are required!", icon="warning")

    def end_program(self):
        self.clients.save_in_file()

    def show_sign_transaction(self):
        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=0)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)
        self.app.grid_rowconfigure(5, weight=0)
        self.app.grid_rowconfigure(6, weight=0)
        self.app.grid_rowconfigure(7, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Sign Transaction", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.network_combobox = customtkinter.CTkComboBox(
            self.app, values=self.networks, command=self.update_tokens_combobox
        )
        self.network_combobox.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.token_combobox = customtkinter.CTkComboBox(self.app, values=self.tokens[self.network_combobox.get()])
        self.token_combobox.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.recipient_entry = customtkinter.CTkEntry(self.app, placeholder_text="Recipient Address")
        self.recipient_entry.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.amount_entry = customtkinter.CTkEntry(self.app, placeholder_text="Amount")
        self.amount_entry.grid(row=4, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.sign_button = customtkinter.CTkButton(
            self.app, text="Sign", command=self.show_send_transaction, **default_button
        )
        self.sign_button.grid(row=5, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.back_button = customtkinter.CTkButton(
            self.app, text="Back", command=self.show_assets, **default_back
        )
        self.back_button.grid(row=6, column=0, padx=20, pady=(20, 5), sticky="ew")

        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=7, column=0)

    def update_tokens_combobox(self, network: str):
        for widget in self.token_combobox.winfo_children():
            widget.destroy()
        self.token_combobox = customtkinter.CTkComboBox(self.app, values=self.tokens[network])
        self.token_combobox.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="ew")

    def show_send_transaction(self):
        recipient = self.recipient_entry.get().strip()
        amount = self.amount_entry.get().strip()
        network = self.network_combobox.get().strip()
        token = self.token_combobox.get().strip()

        if not recipient or not amount:
            messagebox(title="Error", message="All fields are required!", icon="warning")
            return

        try:
            float(amount)
        except ValueError:
            messagebox(title="Error", message="Invalid amount!", icon="warning")
            return

        try:
            Web3.to_checksum_address(recipient)
        except:
            messagebox(title="Error", message="Recipient address is incorrect!", icon="warning")

        balance = self.clients.get_balance(network_name=network, token_name=token)

        if Decimal(amount) > Decimal(balance):
            messagebox(title="Transaction cannot be signed",
                       message=f"Insufficient balance of {token}", icon="warning")
            return

        for widget in self.app.winfo_children():
            widget.destroy()

        self.app.grid_columnconfigure(0, weight=1)
        self.app.grid_columnconfigure(1, weight=0)
        self.app.grid_rowconfigure(0, weight=1)
        self.app.grid_rowconfigure(1, weight=0)
        self.app.grid_rowconfigure(2, weight=0)
        self.app.grid_rowconfigure(3, weight=0)
        self.app.grid_rowconfigure(4, weight=0)
        self.app.grid_rowconfigure(5, weight=0)
        self.app.grid_rowconfigure(6, weight=0)
        self.app.grid_rowconfigure(7, weight=0)

        self.title_label = customtkinter.CTkLabel(self.app, text="Send Transaction", font=("Century Gothic", 26))
        self.title_label.grid(row=0, column=0, pady=(20, 10))

        self.recipient_label = customtkinter.CTkLabel(self.app,
                                                      text=f"Recipient Address: {recipient[:7]}...{recipient[-5:]}",
                                                      font=("Century Gothic", 18))
        self.recipient_label.grid(row=1, column=0, padx=20, pady=(5, 5), sticky="w")

        self.amount_label = customtkinter.CTkLabel(self.app, text=f"Amount: {amount} {token}",
                                                   font=("Century Gothic", 18))
        self.amount_label.grid(row=2, column=0, padx=20, pady=(5, 5), sticky="w")

        self.gas_price_label = customtkinter.CTkLabel(self.app,
                                                      text=f"Estimated Gas Price: "
                                                           + "{0:.18f}".format(
                                                          self.clients.get_gas(network=network, token=token,
                                                                               recipient=recipient, amount=amount))
                                                           + f" {self.clients.clients_dict[network].network.native_coin_symbol}",
                                                      font=("Century Gothic", 18))
        self.gas_price_label.grid(row=3, column=0, padx=20, pady=(5, 5), sticky="w")

        self.send_button = customtkinter.CTkButton(
            self.app, text="Send", command=self.send_transaction, **default_button
        )
        self.send_button.grid(row=4, column=0, padx=20, pady=(5, 5), sticky="ew")

        self.back_button = customtkinter.CTkButton(
            self.app, text="Back", command=self.show_sign_transaction, **default_back
        )
        self.back_button.grid(row=5, column=0, padx=20, pady=(20, 5), sticky="ew")

        self.bottom_spacer_label = customtkinter.CTkLabel(self.app, text="")
        self.bottom_spacer_label.grid(row=6, column=0)

        self.recipient = recipient
        self.amount = amount
        self.network = network
        self.token = token

    def send_transaction(self):
        recipient = self.recipient
        amount = self.amount
        network = self.network
        token = self.token

        successful, tx_hash = self.clients.send_transaction(network=network, token=token, recipient=recipient,
                                                amount=amount)

        if successful:
            messagebox(title="Transaction", message=f"Transaction sent successfully!\nTransaction Hash: {tx_hash}")
            self.show_assets()
        else:
            messagebox(title="Error", message="Transaction failed!", icon="warning")


if __name__ == "__main__":
    application = Application()
    try:
        application.app.mainloop()
    except Exception as ex:
        print(ex)
    application.end_program()
