from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QRect
from utils import QVC, return_data, write_data, get_profile, Encryption
import sys, platform

def no_abort(a, b, c):
    sys.__excepthook__(a, b, c)
sys.excepthook = no_abort


class HomePage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(HomePage, self).__init__(parent)
        self.trade_partners, self.jobs, self.projects = [], [], []
        self.setupUi(self)

    def setupUi(self, homepage):


        self.homepage = homepage
        self.homepage.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.homepage.setGeometry(QtCore.QRect(60, 0, 1041, 601))
        self.tasks_card = QtWidgets.QWidget(self.homepage)
        self.tasks_card.setGeometry(QtCore.QRect(30, 110, 991, 461))
        self.tasks_card.setStyleSheet("background-color: #232323;border-radius: 20px;border: 1px solid #2e2d2d;")
        self.scrollArea = QtWidgets.QScrollArea(self.tasks_card)
        self.scrollArea.setGeometry(QtCore.QRect(20, 30, 951, 421))
        self.scrollArea.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.scrollArea.setStyleSheet("border:none;")
        self.scrollArea.setWidgetResizable(True)
        self.scrollAreaWidgetContents = QtWidgets.QWidget()
        self.scrollAreaWidgetContents.setGeometry(QtCore.QRect(0, 0, 951, 421))
        self.verticalLayout = QtWidgets.QVBoxLayout(self.scrollAreaWidgetContents)
        self.verticalLayout.setContentsMargins(0, -1, 0, -1)
        self.verticalLayout.setSpacing(2)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.image_table_header = QtWidgets.QLabel(self.tasks_card)
        self.image_table_header.setGeometry(QtCore.QRect(40, 7, 51, 31))
        self.image_table_header.setText("Image")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15) if platform.system() == "Darwin" else font.setPointSize(15 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.image_table_header.setFont(font)
        self.image_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.product_table_header = QtWidgets.QLabel(self.tasks_card)
        self.product_table_header.setGeometry(QtCore.QRect(240, 7, 61, 31))
        self.product_table_header.setFont(font)
        self.product_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.product_table_header.setText("Product")
        self.profile_table_header = QtWidgets.QLabel(self.tasks_card)
        self.profile_table_header.setGeometry(QtCore.QRect(590, 7, 61, 31))
        self.profile_table_header.setFont(font)
        self.profile_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.profile_table_header.setText("Profile")
        self.status_table_header = QtWidgets.QLabel(self.tasks_card)
        self.status_table_header.setGeometry(QtCore.QRect(650, 7, 61, 31))
        self.status_table_header.setFont(font)
        self.status_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.status_table_header.setText("Status")
        self.actions_table_header = QtWidgets.QLabel(self.tasks_card)
        self.actions_table_header.setGeometry(QtCore.QRect(890, 7, 61, 31))
        self.actions_table_header.setFont(font)
        self.actions_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.actions_table_header.setText("Actions")
        self.site_table_header = QtWidgets.QLabel(self.tasks_card)
        self.site_table_header.setGeometry(QtCore.QRect(160, 7, 61, 31))
        self.site_table_header.setFont(font)
        self.site_table_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.site_table_header.setText("Site")
        self.id_header = QtWidgets.QLabel(self.tasks_card)
        self.id_header.setGeometry(QtCore.QRect(110, 7, 31, 31))
        self.id_header.setFont(font)
        self.id_header.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.id_header.setText("ID")
        self.tasks_header = QtWidgets.QLabel(self.homepage)
        self.tasks_header.setGeometry(QtCore.QRect(30, 10, 61, 31))
        self.tasks_header.setText("Tasks")
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(22) if platform.system() == "Darwin" else font.setPointSize(22 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.tasks_header.setFont(font)
        self.tasks_header.setStyleSheet("color: rgb(234, 239, 239);")
        self.checkouts_card = QtWidgets.QWidget(self.homepage)
        self.checkouts_card.setGeometry(QtCore.QRect(440, 45, 171, 51))
        self.checkouts_card.setStyleSheet("background-color: #232323;border-radius: 10px;border: 1px solid #2e2d2d;")
        self.checkouts_label = QtWidgets.QLabel(self.checkouts_card)
        self.checkouts_label.setGeometry(QtCore.QRect(78, 10, 81, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(16) if platform.system() == "Darwin" else font.setPointSize(16 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.checkouts_label.setFont(font)
        self.checkouts_label.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.checkouts_label.setText("Checkouts")
        self.checkouts_icon = QtWidgets.QLabel(self.checkouts_card)
        self.checkouts_icon.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.checkouts_icon.setStyleSheet("border: none;")
        self.checkouts_icon.setText("")
        self.checkouts_icon.setPixmap(QtGui.QPixmap(":/images/success.png"))
        self.checkouts_icon.setScaledContents(True)
        self.tasks_total_card = QtWidgets.QWidget(self.homepage)
        self.tasks_total_card.setGeometry(QtCore.QRect(30, 45, 181, 51))
        self.tasks_total_card.setStyleSheet("background-color: #232323;border-radius: 10px;border: 1px solid #2e2d2d;")
        self.tasks_total_label = QtWidgets.QLabel(self.tasks_total_card)
        self.tasks_total_label.setGeometry(QtCore.QRect(80, 10, 91, 31))
        self.tasks_total_label.setFont(font)
        self.tasks_total_label.setStyleSheet("color: rgb(234, 239, 239);border: none;")
        self.tasks_total_label.setText("Total Tasks")
        self.tasks_total_icon = QtWidgets.QLabel(self.tasks_total_card)
        self.tasks_total_icon.setGeometry(QtCore.QRect(10, 10, 31, 31))
        self.tasks_total_icon.setStyleSheet("border: none;")
        self.tasks_total_icon.setText("")
        self.tasks_total_icon.setPixmap(QtGui.QPixmap(":/images/tasks.png"))
        self.tasks_total_icon.setScaledContents(True)

        QtCore.QMetaObject.connectSlotsByName(homepage)

    @QtCore.pyqtSlot()
    def on_pressed(self):
        settings = settings_data

    def add_trade_partner(self):
        for task in self.tasks:
            try:
                task.start(None)
            except:
                pass

    def list_of_trade_partners(self):
        pass


#Current Projects
class RealTimePage(QtWidgets.QWidget):

    def __init__(self,parent=None):
        super(RealTimePage, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, profilespage):
       self.widget = QtWidgets.QLabel(profilespage)

    
    def same_shipping_checkbox_clicked(self):
        if self.same_shipping_checkbox.isChecked():
            self.billing_country_box.setCurrentIndex(self.billing_country_box.findText(self.shipping_country_box.currentText()))
            self.billing_fname_edit.setText(self.shipping_fname_edit.text())
            self.billing_lname_edit.setText(self.shipping_lname_edit.text())
            self.billing_email_edit.setText(self.shipping_email_edit.text())
            self.billing_phone_edit.setText(self.shipping_phone_edit.text())
            self.billing_address1_edit.setText(self.shipping_address1_edit.text())
            self.billing_address2_edit.setText(self.shipping_address2_edit.text())
            self.billing_city_edit.setText(self.shipping_city_edit.text())
            self.billing_zipcode_edit.setText(self.shipping_zipcode_edit.text())
            self.billing_state_box.setCurrentIndex(self.billing_state_box.findText(self.shipping_state_box.currentText()))


#Old Projects
class WarrantyPage(QtWidgets.QWidget):

    def __init__(self, parent=None):
        super(WarrantyPage, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, profilespage):

        # Project Choice
        # Default
        self.profilespage = profilespage
        self.profilespage.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.profilespage.setGeometry(QtCore.QRect(60, 0, 1041, 601))
        self.profilespage.setStyleSheet(
            "QComboBox::drop-down {    border: 0px;}QComboBox::down-arrow {    image: url(:/images/down_icon.png);    width: 14px;    height: 14px;}QComboBox{    padding: 1px 0px 1px 3px;}QLineEdit:focus {   border: none;   outline: none;}")
        self.shipping_card = QtWidgets.QWidget(self.profilespage)
        self.shipping_card.setGeometry(QtCore.QRect(30, 70, 313, 501))
        self.shipping_card.setStyleSheet("background-color: #232323;border-radius: 20px;border: 1px solid #2e2d2d;")
        self.shipping_fname_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_fname_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_fname_edit.setGeometry(QtCore.QRect(30, 50, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13 * .75)
        font.setFamily("Arial")
        self.shipping_fname_edit.setFont(font)
        self.shipping_fname_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_fname_edit.setPlaceholderText("First Name")
        self.shipping_header = QtWidgets.QLabel(self.shipping_card)
        self.shipping_header.setGeometry(QtCore.QRect(20, 10, 81, 31))
        font.setPointSize(18) if platform.system() == "Darwin" else font.setPointSize(18 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.shipping_header.setFont(font)
        self.shipping_header.setStyleSheet("color: rgb(212, 214, 214);border:  none;")
        self.shipping_header.setText("Shipping")
        self.shipping_lname_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_lname_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_lname_edit.setGeometry(QtCore.QRect(170, 50, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13 * .75)
        font.setFamily("Arial")
        self.shipping_lname_edit.setFont(font)
        self.shipping_lname_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_lname_edit.setPlaceholderText("Last Name")
        self.shipping_email_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_email_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_email_edit.setGeometry(QtCore.QRect(30, 100, 253, 21))
        self.shipping_email_edit.setFont(font)
        self.shipping_email_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_email_edit.setPlaceholderText("Email Address")
        self.shipping_phone_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_phone_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_phone_edit.setGeometry(QtCore.QRect(30, 150, 253, 21))
        self.shipping_phone_edit.setFont(font)
        self.shipping_phone_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_phone_edit.setPlaceholderText("Phone Number")
        self.shipping_address1_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_address1_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_address1_edit.setGeometry(QtCore.QRect(30, 200, 151, 21))
        self.shipping_address1_edit.setFont(font)
        self.shipping_address1_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_address1_edit.setPlaceholderText("Address 1")
        self.shipping_address2_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_address2_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_address2_edit.setGeometry(QtCore.QRect(208, 200, 75, 21))
        self.shipping_address2_edit.setFont(font)
        self.shipping_address2_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_address2_edit.setPlaceholderText("Address 2")
        self.shipping_city_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_city_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_city_edit.setGeometry(QtCore.QRect(30, 250, 151, 21))
        self.shipping_city_edit.setFont(font)
        self.shipping_city_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_city_edit.setPlaceholderText("City")
        self.shipping_zipcode_edit = QtWidgets.QLineEdit(self.shipping_card)
        self.shipping_zipcode_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.shipping_zipcode_edit.setGeometry(QtCore.QRect(208, 250, 75, 21))
        self.shipping_zipcode_edit.setFont(font)
        self.shipping_zipcode_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_zipcode_edit.setPlaceholderText("Zip Code")
        self.shipping_state_box = QtWidgets.QComboBox(self.shipping_card)
        self.shipping_state_box.setGeometry(QtCore.QRect(30, 300, 253, 26))
        self.shipping_state_box.setFont(font)
        self.shipping_state_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_state_box.addItem("State")
        self.shipping_country_box = QtWidgets.QComboBox(self.shipping_card)
        self.shipping_country_box.setGeometry(QtCore.QRect(30, 360, 253, 26))
        self.shipping_country_box.setFont(font)
        self.shipping_country_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.shipping_country_box.addItem("Country")
        self.shipping_country_box.addItem("United States")
        self.profiles_header = QtWidgets.QLabel(self.profilespage)
        self.profiles_header.setGeometry(QtCore.QRect(30, 10, 81, 31))
        font.setPointSize(22) if platform.system() == "Darwin" else font.setPointSize(22 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.profiles_header.setFont(font)
        self.profiles_header.setStyleSheet("color: rgb(234, 239, 239);")
        self.profiles_header.setText("Profiles")
        self.billing_card = QtWidgets.QWidget(self.profilespage)
        self.billing_card.setGeometry(QtCore.QRect(365, 70, 313, 501))
        self.billing_card.setStyleSheet("background-color: #232323;border-radius: 20px;border: 1px solid #2e2d2d;")
        self.billing_fname_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_fname_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_fname_edit.setGeometry(QtCore.QRect(30, 50, 113, 21))
        font = QtGui.QFont()
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13 * .75)
        font.setFamily("Arial")
        self.billing_fname_edit.setFont(font)
        self.billing_fname_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_fname_edit.setPlaceholderText("First Name")
        self.billing_header = QtWidgets.QLabel(self.billing_card)
        self.billing_header.setGeometry(QtCore.QRect(20, 10, 51, 31))
        font.setPointSize(18) if platform.system() == "Darwin" else font.setPointSize(18 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.billing_header.setFont(font)
        self.billing_header.setStyleSheet("color: rgb(212, 214, 214);border:  none;")
        self.billing_header.setText("Billing")
        font = QtGui.QFont()
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13 * .75)
        font.setFamily("Arial")
        self.billing_lname_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_lname_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_lname_edit.setGeometry(QtCore.QRect(170, 50, 113, 21))
        self.billing_lname_edit.setFont(font)
        self.billing_lname_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_lname_edit.setPlaceholderText("Last Name")
        self.billing_email_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_email_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_email_edit.setGeometry(QtCore.QRect(30, 100, 253, 21))
        self.billing_email_edit.setFont(font)
        self.billing_email_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_email_edit.setPlaceholderText("Email Address")
        self.billing_phone_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_phone_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_phone_edit.setGeometry(QtCore.QRect(30, 150, 253, 21))
        self.billing_phone_edit.setFont(font)
        self.billing_phone_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_phone_edit.setPlaceholderText("Phone Number")
        self.billing_address1_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_address1_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_address1_edit.setGeometry(QtCore.QRect(30, 200, 151, 21))
        self.billing_address1_edit.setFont(font)
        self.billing_address1_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_address1_edit.setPlaceholderText("Address 1")
        self.billing_address2_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_address2_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_address2_edit.setGeometry(QtCore.QRect(208, 200, 75, 21))
        self.billing_address2_edit.setFont(font)
        self.billing_address2_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_address2_edit.setPlaceholderText("Address 2")
        self.billing_city_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_city_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_city_edit.setGeometry(QtCore.QRect(30, 250, 151, 21))
        self.billing_city_edit.setFont(font)
        self.billing_city_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_city_edit.setPlaceholderText("City")
        self.billing_zipcode_edit = QtWidgets.QLineEdit(self.billing_card)
        self.billing_zipcode_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.billing_zipcode_edit.setGeometry(QtCore.QRect(208, 250, 75, 21))
        self.billing_zipcode_edit.setFont(font)
        self.billing_zipcode_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_zipcode_edit.setPlaceholderText("Zip Code")
        self.billing_state_box = QtWidgets.QComboBox(self.billing_card)
        self.billing_state_box.setGeometry(QtCore.QRect(30, 300, 253, 26))
        self.billing_state_box.setFont(font)
        self.billing_state_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_state_box.addItem("State")
        self.billing_country_box = QtWidgets.QComboBox(self.billing_card)
        self.billing_country_box.setGeometry(QtCore.QRect(30, 360, 253, 26))
        self.billing_country_box.setFont(font)
        self.billing_country_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.billing_country_box.addItem("Country")
        self.billing_country_box.addItem("United States")
        self.same_shipping_checkbox = QtWidgets.QCheckBox(self.billing_card)
        self.same_shipping_checkbox.setGeometry(QtCore.QRect(160, 16, 131, 20))
        self.same_shipping_checkbox.setFont(font)
        self.same_shipping_checkbox.setStyleSheet("border:none;color: rgb(234, 239, 239);")
        self.same_shipping_checkbox.setText("Same as shipping")
        self.same_shipping_checkbox.stateChanged.connect(self.same_shipping_checkbox_clicked)
        self.tasks_card_3 = QtWidgets.QWidget(self.profilespage)
        self.tasks_card_3.setGeometry(QtCore.QRect(700, 70, 313, 501))
        self.tasks_card_3.setStyleSheet("background-color: #232323;border-radius: 20px;border: 1px solid #2e2d2d;")
        self.payment_header = QtWidgets.QLabel(self.tasks_card_3)
        self.payment_header.setGeometry(QtCore.QRect(20, 10, 81, 31))
        font.setPointSize(18) if platform.system() == "Darwin" else font.setPointSize(18 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.payment_header.setFont(font)
        self.payment_header.setStyleSheet("color: rgb(212, 214, 214);border:  none;")
        self.payment_header.setText("Payment")
        self.cardnumber_edit = QtWidgets.QLineEdit(self.tasks_card_3)
        self.cardnumber_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.cardnumber_edit.setGeometry(QtCore.QRect(30, 100, 151, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        self.cardnumber_edit.setFont(font)
        self.cardnumber_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.cardnumber_edit.setPlaceholderText("Card Number")
        self.cardcvv_edit = QtWidgets.QLineEdit(self.tasks_card_3)
        self.cardcvv_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.cardcvv_edit.setGeometry(QtCore.QRect(208, 100, 75, 21))
        self.cardcvv_edit.setFont(font)
        self.cardcvv_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.cardcvv_edit.setPlaceholderText("CVV")
        self.save_btn = QtWidgets.QPushButton(self.tasks_card_3)
        self.save_btn.setGeometry(QtCore.QRect(70, 300, 86, 32))
        self.save_btn.setFont(font)
        self.save_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.save_btn.setStyleSheet(
            "color: #FFFFFF;background-color: #5D43FB;border-radius: 10px;border: 1px solid #2e2d2d;")
        self.save_btn.setText("Save")
        self.cardtype_box = QtWidgets.QComboBox(self.tasks_card_3)
        self.cardtype_box.setGeometry(QtCore.QRect(30, 50, 253, 26))
        self.cardtype_box.setFont(font)
        self.cardtype_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.cardtype_box.addItem("Card Type")
        self.cardmonth_box = QtWidgets.QComboBox(self.tasks_card_3)
        self.cardmonth_box.setGeometry(QtCore.QRect(30, 150, 113, 26))
        self.cardmonth_box.setFont(font)
        self.cardmonth_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.cardmonth_box.addItem("Month")
        self.cardyear_box = QtWidgets.QComboBox(self.tasks_card_3)
        self.cardyear_box.setGeometry(QtCore.QRect(170, 150, 113, 26))
        self.cardyear_box.setFont(font)
        self.cardyear_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.cardyear_box.addItem("Year")
        self.profile_header = QtWidgets.QLabel(self.tasks_card_3)
        self.profile_header.setGeometry(QtCore.QRect(20, 220, 81, 31))
        font.setPointSize(18) if platform.system() == "Darwin" else font.setPointSize(18 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.profile_header.setFont(font)
        self.profile_header.setStyleSheet("color: rgb(212, 214, 214);border:  none;")
        self.profile_header.setText("Profile")
        self.profilename_edit = QtWidgets.QLineEdit(self.tasks_card_3)
        self.profilename_edit.setAttribute(QtCore.Qt.WA_MacShowFocusRect, 0)
        self.profilename_edit.setGeometry(QtCore.QRect(30, 260, 253, 21))
        font = QtGui.QFont()
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13 * .75)
        font.setFamily("Arial")
        self.profilename_edit.setFont(font)
        self.profilename_edit.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.profilename_edit.setPlaceholderText("Profile Name")
        self.loadprofile_box = QtWidgets.QComboBox(self.tasks_card_3)
        self.loadprofile_box.setGeometry(QtCore.QRect(30, 350, 253, 26))
        self.loadprofile_box.setFont(font)
        self.loadprofile_box.setStyleSheet(
            "outline: 0;border: 1px solid #5D43FB;border-width: 0 0 2px;color: rgb(234, 239, 239);")
        self.loadprofile_box.addItem("Load Profile")
        self.loadprofile_box.currentTextChanged.connect(self.load_profile)
        self.delete_btn = QtWidgets.QPushButton(self.tasks_card_3)
        self.delete_btn.setGeometry(QtCore.QRect(167, 300, 86, 32))
        self.delete_btn.setFont(font)
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_btn.setStyleSheet(
            "color: #FFFFFF;background-color: #5D43FB;border-radius: 10px;border: 1px solid #2e2d2d;")
        self.delete_btn.setText("Delete")
        self.set_data()
        QtCore.QMetaObject.connectSlotsByName(profilespage)

    def set_data(self):
        for state in ["AL", "AK", "AS", "AZ", "AR", "CA", "CO", "CT", "DE", "DC", "FM", "FL", "GA", "GU", "HI", "ID",
                      "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MH", "MD", "MA", "MI", "MN", "MS", "MO", "MT", "NE",
                      "NV", "NH", "NJ", "NM", "NY", "NC", "ND", "MP", "OH", "OK", "OR", "PW", "PA", "PR", "RI", "SC",
                      "SD", "TN", "TX", "UT", "VT", "VI", "VA", "WA", "WV", "WI", "WY"]:
            self.shipping_state_box.addItem(state)
            self.billing_state_box.addItem(state)
        for month in range(1, 13):
            self.cardmonth_box.addItem(str(month)) if month > 9 else self.cardmonth_box.addItem("0" + str(month))
        for year in range(2020, 2031):
            self.cardyear_box.addItem(str(year))
        for card_type in ["Visa", "Mastercard", "American Express", "Discover"]:
            self.cardtype_box.addItem(card_type)
        profiles = return_data("./data/profiles.json")
        for profile in profiles:
            profile_name = profile["profile_name"]
            self.loadprofile_box.addItem(profile_name)

    def same_shipping_checkbox_clicked(self):
        if self.same_shipping_checkbox.isChecked():
            self.billing_country_box.setCurrentIndex(
                self.billing_country_box.findText(self.shipping_country_box.currentText()))
            self.billing_fname_edit.setText(self.shipping_fname_edit.text())
            self.billing_lname_edit.setText(self.shipping_lname_edit.text())
            self.billing_email_edit.setText(self.shipping_email_edit.text())
            self.billing_phone_edit.setText(self.shipping_phone_edit.text())
            self.billing_address1_edit.setText(self.shipping_address1_edit.text())
            self.billing_address2_edit.setText(self.shipping_address2_edit.text())
            self.billing_city_edit.setText(self.shipping_city_edit.text())
            self.billing_zipcode_edit.setText(self.shipping_zipcode_edit.text())
            self.billing_state_box.setCurrentIndex(
                self.billing_state_box.findText(self.shipping_state_box.currentText()))

    def load_profile(self):
        profile_name = self.loadprofile_box.currentText()
        p = get_profile(profile_name)
        if p is not None:
            self.profilename_edit.setText(p["profile_name"])
            self.shipping_fname_edit.setText(p["shipping_fname"])
            self.shipping_lname_edit.setText(p["shipping_lname"])
            self.shipping_email_edit.setText(p["shipping_email"])
            self.shipping_phone_edit.setText(p["shipping_phone"])
            self.shipping_address1_edit.setText(p["shipping_a1"])
            self.shipping_address2_edit.setText(p["shipping_a2"])
            self.shipping_city_edit.setText(p["shipping_city"])
            self.shipping_zipcode_edit.setText(p["shipping_zipcode"])
            self.shipping_state_box.setCurrentIndex(self.shipping_state_box.findText(p["shipping_state"]))
            self.shipping_country_box.setCurrentIndex(self.shipping_country_box.findText(p["shipping_country"]))
            self.billing_fname_edit.setText(p["billing_fname"])
            self.billing_lname_edit.setText(p["billing_lname"])
            self.billing_email_edit.setText(p["billing_email"])
            self.billing_phone_edit.setText(p["billing_phone"])
            self.billing_address1_edit.setText(p["billing_a1"])
            self.billing_address2_edit.setText(p["billing_a2"])
            self.billing_city_edit.setText(p["billing_city"])
            self.billing_zipcode_edit.setText(p["billing_zipcode"])
            self.billing_state_box.setCurrentIndex(self.billing_state_box.findText(p["billing_state"]))
            self.billing_country_box.setCurrentIndex(self.billing_country_box.findText(p["billing_country"]))
            self.cardnumber_edit.setText(p["card_number"])
            self.cardmonth_box.setCurrentIndex(self.cardmonth_box.findText(p["card_month"]))
            self.cardyear_box.setCurrentIndex(self.cardyear_box.findText(p["card_year"]))
            self.cardtype_box.setCurrentIndex(self.cardtype_box.findText(p["card_type"]))
            self.cardcvv_edit.setText(p["card_cvv"])
        return

    def save_warranty(self):
        profile_name = self.profilename_edit.text()
        profile_data = {
            "profile_name": profile_name,
            "shipping_fname": self.shipping_fname_edit.text(),
            "shipping_lname": self.shipping_lname_edit.text(),
            "shipping_email": self.shipping_email_edit.text(),
            "shipping_phone": self.shipping_phone_edit.text(),
            "shipping_a1": self.shipping_address1_edit.text(),
            "shipping_a2": self.shipping_address2_edit.text(),
            "shipping_city": self.shipping_city_edit.text(),
            "shipping_zipcode": self.shipping_zipcode_edit.text(),
            "shipping_state": self.shipping_state_box.currentText(),
            "shipping_country": self.shipping_country_box.currentText(),
            "billing_fname": self.billing_fname_edit.text(),
            "billing_lname": self.billing_lname_edit.text(),
            "billing_email": self.billing_email_edit.text(),
            "billing_phone": self.billing_phone_edit.text(),
            "billing_a1": self.billing_address1_edit.text(),
            "billing_a2": self.billing_address2_edit.text(),
            "billing_city": self.billing_city_edit.text(),
            "billing_zipcode": self.billing_zipcode_edit.text(),
            "billing_state": self.billing_state_box.currentText(),
            "billing_country": self.billing_country_box.currentText(),
            "card_number": (Encryption().encrypt(self.cardnumber_edit.text())).decode("utf-8"),
            "card_month": self.cardmonth_box.currentText(),
            "card_year": self.cardyear_box.currentText(),
            "card_type": self.cardtype_box.currentText(),
            "card_cvv": self.cardcvv_edit.text()
        }
        profiles = return_data("./data/profiles.json")
        for p in profiles:
            if p["profile_name"] == profile_name:
                profiles.remove(p)
                break
        profiles.append(profile_data)
        write_data("./data/profiles.json", profiles)
        if self.loadprofile_box.findText(profile_name) == -1:
            self.loadprofile_box.addItem(profile_name)
        QtWidgets.QMessageBox.information(self, "Phoenix Bot", "Saved Profile")


class SettingPage(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(SettingPage, self).__init__(parent)
        self.setupUi(self)

    def setupUi(self, settingspage):
        self.settings_page = settingspage

    def on_pressed(self, settings_data):
        global settings
        settings = settings_data

    def start_all_tasks(self):
        for task in self.tasks:
            try:
                task.start(None)
            except:
                pass

    def stop_all_tasks(self):
        for task in self.tasks:
            try:
                task.stop(None)
            except:
                pass



class TaskTab(QtWidgets.QWidget):
    def __init__(self, site, product, profile, proxies, monitor_delay, error_delay, max_price, stop_all, parent=None):
        super(TaskTab, self).__init__(parent)
        self.task_id = str(int(tasks_total_count.text()) + 1)
        tasks_total_count.setText(self.task_id)
        self.site, self.product, self.profile, self.proxies, self.monitor_delay, self.error_delay, self.max_price, self.stop_all = site, product, profile, proxies, monitor_delay, error_delay, max_price, stop_all
        self.setupUi(self)
        tasks.append(self)
        tasks_data = return_data("./data/tasks.json")
        task_data = {"task_id": self.task_id, "site": self.site, "product": self.product, "profile": self.profile,
                     "proxies": self.proxies, "monitor_delay": self.monitor_delay, "error_delay": self.error_delay,
                     "max_price": self.max_price}
        tasks_data.append(task_data)
        write_data("./data/tasks.json", tasks_data)

    def setupUi(self, TaskTab):
        self.running = False

        self.TaskTab = TaskTab
        self.TaskTab.setMinimumSize(QtCore.QSize(0, 50))
        self.TaskTab.setMaximumSize(QtCore.QSize(16777215, 50))
        self.TaskTab.setStyleSheet("border-radius: none;")
        self.product_label = QtWidgets.QLabel(self.TaskTab)
        self.product_label.setGeometry(QtCore.QRect(222, 10, 331, 31))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(13) if platform.system() == "Darwin" else font.setPointSize(13 * .75)
        font.setBold(False)
        font.setWeight(50)
        self.product_label.setFont(font)
        self.product_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.profile_label = QtWidgets.QLabel(self.TaskTab)
        self.profile_label.setGeometry(QtCore.QRect(571, 10, 51, 31))
        self.profile_label.setFont(font)
        self.profile_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.status_label = QtWidgets.QLabel(self.TaskTab)
        self.status_label.setGeometry(QtCore.QRect(632, 10, 231, 31))
        self.status_label.setFont(font)
        self.status_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.browser_label = QtWidgets.QLabel(self.TaskTab)
        self.browser_label.setGeometry(QtCore.QRect(632, 10, 231, 31))
        self.browser_label.setFont(font)
        self.browser_label.setStyleSheet("color: rgb(163, 149, 255);")
        self.browser_label.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.browser_label.mousePressEvent = self.open_browser
        self.browser_label.hide()
        self.start_btn = QtWidgets.QLabel(self.TaskTab)
        self.start_btn.setGeometry(QtCore.QRect(870, 15, 16, 16))
        self.start_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.start_btn.setPixmap(QtGui.QPixmap(":/images/play.png"))
        self.start_btn.setScaledContents(True)
        self.start_btn.mousePressEvent = self.start
        self.stop_btn = QtWidgets.QLabel(self.TaskTab)
        self.stop_btn.setGeometry(QtCore.QRect(870, 15, 16, 16))
        self.stop_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.stop_btn.setPixmap(QtGui.QPixmap(":/images/stop.png"))
        self.stop_btn.setScaledContents(True)
        self.stop_btn.mousePressEvent = self.stop
        self.delete_btn = QtWidgets.QLabel(self.TaskTab)
        self.delete_btn.setGeometry(QtCore.QRect(920, 15, 16, 16))
        self.delete_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.delete_btn.setPixmap(QtGui.QPixmap(":/images/trash.png"))
        self.delete_btn.setScaledContents(True)
        self.delete_btn.mousePressEvent = self.delete
        self.edit_btn = QtWidgets.QLabel(self.TaskTab)
        self.edit_btn.setGeometry(QtCore.QRect(895, 15, 16, 16))
        self.edit_btn.setCursor(QtGui.QCursor(QtCore.Qt.PointingHandCursor))
        self.edit_btn.setPixmap(QtGui.QPixmap(":/images/edit.png"))
        self.edit_btn.setScaledContents(True)
        self.edit_btn.mousePressEvent = self.edit
        self.image = QtWidgets.QLabel(self.TaskTab)
        self.image.setGeometry(QtCore.QRect(20, 0, 50, 50))
        self.image.setPixmap(QtGui.QPixmap(":/images/no_image.png"))
        self.image.setScaledContents(True)
        self.site_label = QtWidgets.QLabel(self.TaskTab)
        self.site_label.setGeometry(QtCore.QRect(140, 10, 61, 31))
        self.site_label.setFont(font)
        self.site_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.id_label = QtWidgets.QLabel(self.TaskTab)
        self.id_label.setGeometry(QtCore.QRect(90, 10, 31, 31))
        self.id_label.setFont(font)
        self.id_label.setStyleSheet("color: rgb(234, 239, 239);")
        self.stop_btn.raise_()
        self.product_label.raise_()
        self.profile_label.raise_()
        self.browser_label.raise_()
        self.start_btn.raise_()
        self.delete_btn.raise_()
        self.image.raise_()
        self.site_label.raise_()
        self.monitor_delay_label = QtWidgets.QLabel(self.TaskTab)
        self.monitor_delay_label.hide()
        self.error_delay_label = QtWidgets.QLabel(self.TaskTab)
        self.error_delay_label.hide()
        self.max_price_label = QtWidgets.QLabel(self.TaskTab)
        self.max_price_label.hide()
        self.proxies_label = QtWidgets.QLabel(self.TaskTab)
        self.proxies_label.hide()
        self.load_labels()

    def load_labels(self):
        self.id_label.setText(self.task_id)
        self.product_label.setText(self.product)
        self.profile_label.setText(self.profile)
        self.proxies_label.setText(self.proxies)
        self.status_label.setText("Idle")
        self.browser_label.setText("Click To Open Browser")
        self.site_label.setText(self.site)
        self.monitor_delay_label.setText(self.monitor_delay)
        self.error_delay_label.setText(self.error_delay)
        self.max_price_label.setText(self.max_price)

    def update_status(self, msg):
        self.status_label.setText(msg["msg"])
        if msg["msg"] == "Browser Ready":
            self.browser_url, self.browser_cookies = msg["url"], msg["cookies"]
            self.running = False
            self.start_btn.raise_()
            self.browser_label.show()
            logger.alt(self.task_id, msg["msg"])
            loop = QtCore.QEventLoop()
            QtCore.QTimer.singleShot(1000, loop.quit)
            loop.exec_()
            self.task.stop()
            return
        if msg["status"] == "idle":
            self.status_label.setStyleSheet("color: rgb(255, 255, 255);")
            logger.normal(self.task_id, msg["msg"])
        elif msg["status"] == "normal":
            self.status_label.setStyleSheet("color: rgb(163, 149, 255);")
            logger.normal(self.task_id, msg["msg"])
        elif msg["status"] == "alt":
            self.status_label.setStyleSheet("color: rgb(242, 166, 137);")
            logger.alt(self.task_id, msg["msg"])
        elif msg["status"] == "error":
            self.status_label.setStyleSheet("color: rgb(252, 81, 81);")
            logger.error(self.task_id, msg["msg"])
        elif msg["status"] == "success":
            self.status_label.setStyleSheet("color: rgb(52, 198, 147);")
            logger.success(self.task_id, msg["msg"])
            self.running = False
            self.start_btn.raise_()
            if settings.buy_one:
                self.stop_all()
            checkouts_count.setText(str(int(checkouts_count.text()) + 1))
        elif msg["status"] == "carted":
            self.status_label.setStyleSheet("color: rgb(163, 149, 255);")
            logger.alt(self.task_id, msg["msg"])
            carted_count.setText(str(int(carted_count.text()) + 1))

    def wait_browser_poll(self):
        # Initiate dialog and block until dismissed
        poll_browser_dialog = PollBrowserDialog(self.parent())
        poll_browser_dialog.exec()

        # set wait condition
        self.task.wait_condition.wakeAll()

        pass

    def update_image(self, image_url):
        self.image_thread = ImageThread(image_url)
        self.image_thread.finished_signal.connect(self.set_image)
        self.image_thread.start()

    def set_image(self, pixmap):
        self.image.setPixmap(pixmap)

    def start(self, event):
        if not self.running:
            self.browser_label.hide()
            self.task = TaskThread()
            self.task.status_signal.connect(self.update_status)
            self.task.image_signal.connect(self.update_image)
            self.task.wait_condition = QtCore.QWaitCondition()

            # Special case for Walmart, not sure if should disambiguate
            # allowing other stores to use functionality
            if self.site == "Walmart":
                self.task.wait_poll_signal.connect(self.wait_browser_poll)

            self.task.set_data(
                self.task_id,
                self.site_label.text(),
                self.product_label.text(),
                self.profile_label.text(),
                self.proxies_label.text(),
                self.monitor_delay_label.text(),
                self.error_delay_label.text(),
                self.max_price_label.text()
            )
            self.task.start()
            self.running = True
            self.stop_btn.raise_()

    def stop(self, event):
        self.task.stop()
        self.running = False
        self.update_status({"msg": "Stopped", "status": "idle"})
        self.start_btn.raise_()


    def update_task(self):
        self.site = self.edit_dialog.site_box.currentText()
        self.product = self.edit_dialog.input_edit.text()
        self.profile = self.edit_dialog.profile_box.currentText()
        self.proxies = self.edit_dialog.proxies_box.currentText()
        self.monitor_delay = self.edit_dialog.monitor_edit.text()
        self.error_delay = self.edit_dialog.error_edit.text()
        self.max_price = self.edit_dialog.price_edit.text()
        self.load_labels()
        self.delete_json()
        tasks_data = return_data("./data/tasks.json")
        task_data = {"task_id": self.task_id, "site": self.site, "product": self.product, "profile": self.profile,
                     "proxies": self.proxies, "monitor_delay": self.monitor_delay, "error_delay": self.error_delay,
                     "max_price": self.max_price}
        tasks_data.append(task_data)
        write_data("./data/tasks.json", tasks_data)
        self.edit_dialog.deleteLater()

    def delete_json(self):
        tasks_data = return_data("./data/tasks.json")
        for task in tasks_data:
            if task["task_id"] == self.task_id:
                tasks_data.remove(task)
                break
        write_data("./data/tasks.json", tasks_data)

    def delete(self, event):
        tasks_total_count.setText(str(int(tasks_total_count.text()) - 1))
        self.delete_json()
        self.TaskTab.deleteLater()

    def open_browser(self, event):
        self.browser_thread = BrowserThread()
        self.browser_thread.set_data(
            self.browser_url,
            self.browser_cookies
        )
        self.browser_thread.start()


class TaskThread(QtCore.QThread):
    status_signal = QtCore.pyqtSignal("PyQt_PyObject")
    image_signal = QtCore.pyqtSignal("PyQt_PyObject")
    wait_poll_signal = QtCore.pyqtSignal()

    def __init__(self):
        QtCore.QThread.__init__(self)

    def set_data(self, task_id, site, product, profile, proxies, monitor_delay, error_delay, max_price):
        self.task_id, self.site, self.product, self.profile, self.proxies, self.monitor_delay, self.error_delay, self.max_price = task_id, site, product, profile, proxies, monitor_delay, error_delay, max_price

    def run(self):
        profile, proxy = get_profile(self.profile), get_proxy(self.proxies)
        if profile == None:
            self.status_signal.emit({"msg": "Invalid profile", "status": "error"})
            return
        if proxy == None:
            self.status_signal.emit({"msg": "Invalid proxy list", "status": "error"})
            return
        if self.site == "Walmart":
            Walmart(self.task_id, self.status_signal, self.image_signal, self.wait_poll_signal, self.wait_condition,
                    self.product, profile, proxy, self.monitor_delay, self.error_delay, self.max_price)
        elif self.site == "Bestbuy":
            BestBuy(self.task_id, self.status_signal, self.image_signal, self.product, profile, proxy,
                    self.monitor_delay, self.error_delay)

    def stop(self):
        self.terminate()


class ImageThread(QtCore.QThread):
    finished_signal = QtCore.pyqtSignal("PyQt_PyObject")

    def __init__(self, image_url):
        self.image_url = image_url
        QtCore.QThread.__init__(self)

    def run(self):
        data = urllib.request.urlopen(self.image_url).read()
        pixmap = QtGui.QPixmap()
        pixmap.loadFromData(data)
        self.finished_signal.emit(pixmap)


class BrowserThread(QtCore.QThread):
    def __init__(self):
        QtCore.QThread.__init__(self)

    def set_data(self, url, cookies):
        self.url, self.cookies = url, cookies

    def run(self):
        open_browser(self.url, self.cookies)
