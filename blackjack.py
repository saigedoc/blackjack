# Импорт необходимых функций
from random import choice
from sys import exit
from os import system
from datetime import datetime as dt
from colorama import init, Fore


class Card(object):
	
	#Класс "Card" отвечает за функции и свойства карт.
	
	def __init__(self, suit, name):
		super(Card, self).__init__()
		"""
		suit - масть
		name - название карты
		
		Все имена:{'2','3','4','5','6','7','8','9','10', "king", "jack", "queen", "ace"},
		где 4 последних соответственно "Король", "Валет", "Дама", "Туз".
		Стоимость карт от 2 до 10 соответсвенно названиям, у Короля Вальта и Дамы по 10, Туз - 11.
		"""
		self.suit = suit
		self.name = name
		if name in ['2','3','4','5','6','7','8','9','10']:
			self.cost = int(name)
		elif name == 'ace':
			self.cost = 11
		else:
			self.cost = 10

	def get_cost(self):
		#Возвращает стоимость карты
		return self.cost

	def get_description(self):
		#Возвращает описание карты в формате [название/масть/стоимость]
		return "[%s, масть - %s, стоимость - %s]" %(self.name,self.suit,self.cost)


class casino(object):
	"""
	Основной класс, отвечающий за главное меню, смену режимов, и основной цикл игры,
	со всеми прилагающимися функциями.
	"""
	def __init__(self, money=1000):
		super(casino, self).__init__()
		"""
		self.color - цвет текста
		init(convert=True) - инициализация цветов для принта
		self.text_interval = 0.08 - 
		self.text_time=True
		self.indent - отступ.
		self.runbool - условие для основного цикла игры .
		self.status - статус режима ("menu"/"game").
		self.money - деньги игрока.
		self.bet - последняя ставка игрока (Используется для действия "сплит", для повторной ставки).
		self.response - переменная содержая в себе ответ игрока, при выборе действия, или выборе ставки.
		self.deck - колода, из которой беруться карты.
		self.croupier_cards - карты Крупье.
		self.player_cards - карты игрока в формате [[рука с картами1], [рука с картами 2], ...].
		self.hand_status_id - отслеживание каждой руки игрока в формате [play,done].
		self.output_text - список строк, который по очерёдно выводит функция game_print().
		self.buttons_name - список названий кнопок.
		self.buttons_func=[self.start_game, self.close] - список функций кнопок, соответствующие названиям.
		"""
		self.color = Fore.GREEN
		if self.color:
			init(convert=True)
		self.text_interval = 0.06
		self.intervals = [self.text_interval,self.text_interval/(8), self.text_interval/(8**2)]
		self.text_time=True
		self.indent=70
		self.min_bet=100
		self.xbet=1.5
		self.runbool=True
		self.status='menu'
		if money <100:
			money=100
		self.money=money
		self.bet=0
		self.response = ''
		self.deck = []
		self.croupier_cards=[]
		self.player_cards=[[]]
		self.hand_status_id = [[0],[]] # play/ done
		self.output_text=[]
		self.buttons_name=["1) Начать","2) Выход"]
		self.buttons_func=[self.start_game, self.close]

	def new_print(self, text, interval=None):
		#print  с возможностью временного интервала между каждым символом.
		if not interval:
			interval=self.text_interval
		t1 = (dt.strftime(dt.now(), "%S %f")).split(' ')
		t1 = float(t1[0]) + ( float(t1[1]) / (10 ** 6) )
		time = self.text_time
		for i in range(len(list(text))):
			while time:
				t2 = (dt.strftime(dt.now(), "%S %f")).split(' ')
				t2 = float(t2[0]) + ( float(t2[1]) / (10 ** 6) )
				if t2 < t1:
					t2 += 60
				if t2 - t1 >= interval: 
					t1 = t2
					time = False
			if i + 1 == len(list(text)):
				print(self.color + list(text)[i])
			else:
				print(self.color + list(text)[i], end = "")
			time = self.text_time

	def main(self):
		#Главный цикл
		while self.runbool:
			if self.status=='game':
				self.game()
			self.game_print()
			self.get_response()

	def print_error(self,error='Неверный ввод.'):
		print('')
		self.new_print(error,interval=self.intervals[2])
		input('Нажмите enter, чтобы продолжить.')

	def game_print(self):
		#Функция вывод текста в консоль
		system("cls")
		for i in self.output_text:
			if len(self.output_text)>10:
				self.new_print(i, interval=self.intervals[2])
			elif len(self.output_text)>4:
				self.new_print(i, interval=self.intervals[1])
			else:
				self.new_print(i)
		print('')
		for i in self.buttons_name:
			if len(self.buttons_name)>10:
				self.new_print(i, interval=self.intervals[2])
			elif len(self.buttons_name)>4:
				self.new_print(i, interval=self.intervals[1])
			else:
				self.new_print(i)
		print('')

	def get_response(self):
		#Функция, получающая ответ игрока и запускающая функцию выбранной кнопки
		self.response = input()
		try:
			self.response=int(self.response)-1
			if self.response<len(self.buttons_func) and self.response >= 0: 
				self.buttons_func[self.response]()
			else:
				self.print_error('Такого действия нету.')
		except:
			self.print_error()
	
	def start_game(self):
		#Выполяняет подготовку перед основной игрой (создать колоду, раздатьк карты)
		self.make_deck()
		self.croupier_cards.append(self.get_card())
		self.croupier_cards.append(self.get_card())
		self.player_cards[0].append(self.get_card())
		self.player_cards[0].append(self.get_card())
		system("cls")
		self.new_print("Ваши деньги: %s" %self.money)
		print('')
		self.bet = input('Ваша ставка: ')
		if self.bet.isdigit():
			self.bet = int(self.bet)
			if self.bet >= self.min_bet and self.bet<=self.money:
				
				self.money -= self.bet
				self.status='game'
			else:
				self.print_error('Вы ввели недопустимую сумму денег. Минимальная ставка - "%s";Максимальная - "%s"' %(self.min_bet,max(self.money,self.min_bet)))
		else:
			self.print_error()

	def make_deck(self):
		"""
		Функция создания колоды.
		Так как в казино используются шафл машинки, считается что колода бесконечная,
		поэтому, собирается 1 колода, которая не может уменьшится, сколько бы карт не брали. 

		Список мастей:
		Diamonds (Бубы / Алмазы)
    	Hearts (Черви / Сердца)
    	Clubs (Трефы / Клубы)
    	Spades (Пики / Лопаты)
		"""
		for name in ['2','3','4','5','6','7','8','9','10', "king", "jack", "queen", "ace"]:
			for suit in ['Diamonds','Hearts','Clubs', 'Spades']:
				self.deck.append(Card(suit,name))

	def game(self):
		"""
		Функция основной логики игры.
		Первое условие проверяет являются ли руки игра законченными (игрок решил больше не брать карты и сделать "пас"),
		если нет, то идёт основная логика, если да, логика финального подсчёта и вывода выйгранных денег.
		
		self.output_text меняется вывод текста
		self.buttons_name название кнопок
		self.buttons_func функции кнопок
		"""
		for i in range(len(self.player_cards)):
			if self.get_sum(index=i)>= 21 and (i not in self.hand_status_id[1]) and not(self.player_cards[i][-1].get_cost() == self.player_cards[i][-2].get_cost()):
				self.hand_status_id[1].append(i)
				self.hand_status_id[0].remove(i)

		if len(self.hand_status_id[1]) != len(self.player_cards):
			self.output_text = ["Ваши деньги: %s" %self.money, '',
				'Рука Крупье:', "[Неизвестно]", self.croupier_cards[1].get_description(),
				"общая стоимость - Неизвестно.",'',
				*[("Ваша рука №%s:\n" %(i+1)) + '\n'.join([j.get_description() for j in self.player_cards[i]]) + '\n' + \
				("Общая стоимость - %s" %( sum([j.get_cost() for j in self.player_cards[i]]))+'\n')\
				for i in range(len(self.player_cards))]]
			self.buttons_name = ['1) Правила.', "2) Пас", "3) Взять ещё карту.", "4) Сплит.", "5) Cдаться."]
			self.buttons_func = [self.print_rules, self.finish, self.player_get_card, self.split, self.give_up]
		else:
			system("cls")
			interval_index=2
			self.new_print('Крупье вскрывает карты.', interval=self.intervals[interval_index])
			z=0
			while sum([i.get_cost() for i in self.croupier_cards])<17:
				z+=1
				self.croupier_cards.append(self.get_card())
			self.new_print("Крупье взял карт:%s" %z, interval=self.intervals[interval_index])
			print('')
			self.new_print("Карты крупье:", interval=self.intervals[interval_index])
			[self.new_print(i.get_description(), interval=self.intervals[interval_index]) for i in self.croupier_cards]
			croupier_sum=sum([i.get_cost() for i in self.croupier_cards])
			self.new_print('Общая сумма карт - %s' %croupier_sum, interval=self.intervals[interval_index])
			print('')
			for i in[("Ваша рука №%s:\n" %(i+1)) + '\n'.join([j.get_description() for j in self.player_cards[i]]) + '\n' + \
				("Общая стоимость - %s" %( sum([j.get_cost() for j in self.player_cards[i]]) )) for i in range(len(self.player_cards))]:
				self.new_print(i, interval=self.intervals[interval_index])
				print('\n')
			print('')
			wins=0
			tie=0
			for i in self.player_cards:
				s=sum([j.get_cost() for j in i])
				if s<=21 and (s>croupier_sum or croupier_sum>21):
					wins+=1
				elif s==croupier_sum or (s>21 and croupier_sum>21):
					tie+=1
			win_money=wins*self.bet*self.xbet+self.bet*tie
			self.new_print('Вы потратили: %s' %(len(self.player_cards)*self.bet), interval=self.intervals[interval_index])
			self.new_print('Ваш выигрыш: %s' %win_money, interval=self.intervals[interval_index])
			self.money+=win_money
			self.new_print('Ваши деньги: %s' %self.money, interval=self.intervals[interval_index])
			print('')
			input('Нажмите enter, чтобы закончить.')
			self.__init__(money=self.money)

	def get_sum(self, index=0):
		#Возвращает сумму стоимостей карт ИГРОКА.
		return sum([i.get_cost() for i in self.player_cards[index]])		

	def player_get_card(self):
		#функция взятия карты игроков в момент игры.
		try:
			if len(self.player_cards)==1:
				index=0
			else:
				index = int(input("Номер руки: "))-1
			
			if index not in self.hand_status_id[1]:
				if index not in self.hand_status_id[0]:
					self.hand_status_id[0].append(index)
				c=self.get_card()
				self.player_cards[index].append(c)
				print('')
				print('')
				print("Вы взяли:",c.get_description())
				input('Нажмите enter, чтобы продожить.')
			else:
				self.print_error('Рука закрыта, выберете другую.')
		except:
			self.print_error()		

	def finish(self):
		#Функция закрывает руку.
		try:
			if len(self.player_cards)==1:
				index=0
			else:
				index = int(input("Номер руки: "))-1
			if index not in self.hand_status_id[1]:
				self.hand_status_id[1].append(index)
				self.hand_status_id[0].remove(index)
			else:
				self.print_error('Рука уже закрыта, выберете другую.')
		except:
			self.print_error()

	def split(self):
		#Функция делает сплит, в случае если на сплит хватает денег.
		if self.bet >= self.min_bet and self.bet<=self.money:
			try:
				if len(self.player_cards)==1:
					index=0
				else:
					index = int(input("Номер руки: "))-1
				if index not in self.hand_status_id[1]:
					if self.player_cards[index][-1].get_cost() == self.player_cards[index][-2].get_cost():
						self.player_cards.append([self.player_cards[index].pop(-1)])
						self.money -= self.bet
					else:
						self.print_error('В этой руке последние карты не одинаковые.')
				else:
					self.print_error('Рука закрыта, выберете другую.')
			except:
				self.print_error()

		else:
			self.print_error('У вас не хватает деньги на ставку, чтобы сделать сплит.')

	def print_rules(self):
		#Пишет правила.
		system('cls')
		interval_index=1
		self.new_print("Игра BlackJack.",interval=self.intervals[interval_index])
		print('')
		self.new_print("Цель иры: набрать 21 очко картами.",interval=self.intervals[interval_index])
		self.new_print("Карты от 2 до 10 стоят соответственно их названию, king, jack, queen стоят по 10, а ace - 11.",interval=self.intervals[interval_index])
		print('')
		self.new_print("Начало игры: Крупье (представитель казино) раздаёт по 2 карты из колоды каждому игроку и себе, "+\
			"причём, все карты открыты для всех игроков кроме одной карты Крупье.",interval=self.intervals[interval_index])
		self.new_print("Колода считается бесконечной, так как казино использует шафл машинку.",interval=self.intervals[interval_index])
		self.new_print("Ход игры: игроки выбирают действия:",interval=self.intervals[interval_index])
		self.new_print("1) Правила - то, что вы сейчас читаете:",interval=self.intervals[interval_index])
		self.new_print("2) Пасс - сделав пасс, вы переходите к финалу и сверяете карты с Крупье.",interval=self.intervals[interval_index])
		self.new_print("3) Взять ещё карту - вы берёте ещё одну карту",interval=self.intervals[interval_index])
		self.new_print("4) Сплит - если две последнии карты в руке одинаковые, вы можете сделать сплит и открыть вторую руку, "+\
			"положив последнюю карту в неё. Тем самым вы играете за двух игроков сразу, и каждый сплит добавляет ставку равнуюю первой.",interval=self.intervals[interval_index])
		self.new_print("5) Сдаться - вы завершаете игру, деньги не возвращаются.",interval=self.intervals[interval_index])
		print('')
		self.new_print("Финал:",interval=self.intervals[interval_index])
		self.new_print("Как только вы сдлали пасс на каждой руке, или на каждой набралось больше или равно 21 очку, то вы переходите к финалу",interval=self.intervals[interval_index])
		self.new_print("Крупье вскрывает карты, и вам станет видно закрытую ранее карту, если у него в сумме получается меньше 17 очков, " +\
			"он будет брать до тех пор, пока не будет 17 или больше.",interval=self.intervals[interval_index])
		self.new_print("Если у вас очков меньше, вы проигрываете и теряете свои деньги.",interval=self.intervals[interval_index])
		self.new_print("Если у вас по ровну очков, или вы оба получили больше 21 очка, вы остаётесь при своих деньгах.",interval=self.intervals[interval_index])
		self.new_print("в ином случае вы получаете выигрыш умноженный на: %s." %self.xbet,interval=self.intervals[interval_index])
		print('')
		self.new_print("Ознакомиться подробнее с правилами всевозможных вариаций BlackJack, можете на вики:",interval=self.intervals[interval_index])	
		self.new_print('"https://ru.wikipedia.org/wiki/Блэкджек"',interval=self.intervals[interval_index])
		print('')
		self.new_print("Приятной игры!",interval=self.intervals[interval_index])	
		input('Нажмите enter чтобы продолжить.')

	def get_card(self):
		#Возвращает случайную карту из колоды.
		if self.deck != []:
			return choice(self.deck)

	def give_up(self):
		#Перезапускает игру, с сохранением денег на момент игры
		self.__init__(money=self.money)

	def close(self):
		#Выключает игру, выключив условие главного цикла.
		self.runbool=False

if __name__ == '__main__':
	#Запуск программы.
	C=casino()
	C.main()