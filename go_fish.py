import unittest
import random

#***************************************************************************#
class Card(object):
	suit_names =  ["Diamonds","Clubs","Hearts","Spades"]
	rank_levels = [1,2,3,4,5,6,7,8,9,10,11,12,13]
	faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}

	def __init__(self, suit=0,rank=2):
		self.suit = self.suit_names[suit]
		if rank in self.faces: # self.rank handles printed representation
			self.rank = self.faces[rank]
		else:
			self.rank = rank
		self.rank_num = rank # To handle winning comparison

	def __str__(self):
		return "{} of {}".format(self.rank,self.suit)

#***************************************************************************#

class Deck(object):
	def __init__(self): # Don't need any input to create a deck of cards
		# This working depends on Card class existing above
		self.cards = []
		for rank in range(1,14):
			for suit in range(4):
				card = Card(suit,rank)
				self.cards.append(card) # appends in a sorted order

	def __str__(self):
		total = []
		for card in self.cards:
			total.append(card.__str__())
		# shows up in whatever order the cards are in
		return "\n".join(total) # returns a multi-line string listing each card

	def pop_card(self, i=-1):
		# removes and returns a card from the Deck
		# default is the last card in the Deck
		return self.cards.pop(i) # this card is no longer in the deck -- taken off

	def shuffle(self):
		random.shuffle(self.cards)

	def replace_card(self, card):
		card_strs = [] # forming an empty list
		for c in self.cards: # each card in self.cards (the initial list)
			card_strs.append(c.__str__()) # appends the string that represents that card to the empty list
		if card.__str__() not in card_strs: # if the string representing this card is not in the list already
			self.cards.append(card) # append it to the list

	def sort_cards(self):
		# Basically, remake the deck in a sorted way
		# This is assuming you cannot have more than the normal 52 cars in a deck
		self.cards = []
		for suit in range(4):
			for rank in range(1,14):
				card = Card(suit,rank)
				self.cards.append(card)
	
	# Deck that takes two parameters representing the number of hands and the number of cards per hand and returns a list of Hands. 
	# If the number of cards per hand is set to -1, all of the cards should be dealt, even if this results in an uneven number of cards per hand.
	# param: numberOfHands, numberOfCards
	# return: handlist - a list of hands
	def deal(self, numberOfHands, numberOfCards):
		handlist = []
		flag = 0
		if numberOfCards == -1:
			numberOfCards = int(len(self.cards)/numberOfHands)
			rest = len(self.cards) - numberOfCards * numberOfHands
			flag = 1
			
		try:
			for i in range(numberOfHands):
				cards = []
				for j in range(numberOfCards):
					cards.append(self.pop_card(0))
				handlist.append(cards)
		except:
			pass
		
		if flag == 1:
			for i in range(rest):
				handlist[i].append(self.pop_card(0))
		return handlist


#***************************************************************************#

class Hand:
	# create the Hand with an initial set of cards
	# param: a list of cards
	def __init__(self, init_cards):
		self.cards = []
		self.cards = init_cards
		self.score = 0

	# add a card to the hand
	# silently fails if the card is already in the hand
	# param: the card to add
	# returns: nothing
	def add_card(self, card):
		flag = 0
		for value in self.cards:
			if value.__str__() == card.__str__():
				flag = 1
				break
		
		if flag == 0:
			self.cards.append(card)
	
	# remove a card from the hand
	# param: the card to remove
	# returns: the card, or None if the card was not in the Hand
	def remove_card(self, card):
		card1 = Card()
		temp = []
		flag = 0
		for val in self.cards:
			if card.__str__() != val.__str__():
				temp.append(val)
			else:
				if flag == 0:
					flag = 1
					card1 = val
				else:
					temp.append(val)
		self.cards = temp
		if flag == 1:
			return card1
		return None

	
	# draw a card from a deck and add it to the hand
	# side effect: the deck will be depleted by one card
	# param: the deck from which to draw
	# returns: nothing
	def draw(self, deck,rank):
		c = deck.pop_card()
		self.add_card(c)
		print(c.rank_num)
		if c.rank_num==rank:
			return 0
		return 1
	# looks for pairs of cards in a hand and removes them.
	# param: nothing
	# return: nothing
	def remove_pairs(self):
		faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}
		for rank in range(1, 14):
			counter = 0
			temp = []
			for card in self.cards:
				if rank in faces:
					if card.rank == faces[rank]:
						temp.append(card)
						counter += 1
				else:	 
					if card.rank == rank:
						temp.append(card)
						counter += 1
				if counter == 2:
					self.remove_card(temp[0])
					self.remove_card(temp[1])
	
	# display the cards in the hand
	def display(self):
		for card in self.cards:
			print(card)
	#check the input rank 
	def check(self,number):
		for card in self.cards:
			if number==card.rank_num:
			    return 0
		return 1
	
	# steal card from other player
	# param: hand - other player's hand
	#		 rank - the desired rank 
	# return: True - if desired rank is in hand
	#		  False - if desired rank not in hand
	#def rank_change(number):
	    
	def go_fish(self,hand,rank):
		flag = 0
		for card in hand.cards:
			if card.rank_num == rank:
				self.add_card(hand.remove_card(card))
				flag = 1
		if flag == 0:
			print("Go Fish!")
			return False
		return True
	
	def remove_four(self):
		faces = {1:"Ace",11:"Jack",12:"Queen",13:"King"}
		for rank in range(1, 14):
			counter = 0
			temp = []
			for card in self.cards:
				if rank in faces:
					if card.rank == faces[rank]:
						temp.append(card)
						counter += 1
				else:	 
					if card.rank_num == rank:
						temp.append(card)
						counter += 1
				if counter == 4:
					self.remove_card(temp[0])
					self.remove_card(temp[1])
					self.remove_card(temp[2])
					self.remove_card(temp[3])
					print("Four rank "+str(temp[0].rank)+" are removed.")
					self.score += 1
					counter = 0
#***************************************************************************#

def start_game():
	# player1 : -1, player2: 1
	turn = -1
	player = {"-1":"Player 1", "1": "Player 2"}
	# initialize deck and hands
	deck = Deck()
	# for i in range(36):
	#  	deck.pop_card()
	deck.shuffle()

	handlist = deck.deal(2,7)
	hand1 = Hand(handlist[0])
	hand2 = Hand(handlist[1])
	print(type(hand2))

	while len(deck.cards) != 0 or len(hand1.cards) != 0 or len(hand2.cards) != 0:
		print("****************")
		print("Player 1 has: ")
		hand1.display()
		print("****************")
		print("Player 2 has: ")
		hand2.display()
		# Ask input
		# if Player 1's turn
		print("****************")
		print(player[str(turn)]+"'s turn")
		print("****************")
		while turn == -1:
			hand1.remove_four()
			rank=0
			if len(hand1.cards)!=0:
			    while hand1.check(rank):
				    rank = int(input("Please choose a card rank you would like to ask the other player if they have (between 1-13): "))
					
			while hand1.go_fish(hand2,rank) and len(hand1.cards)!=0:
				# remove 4 same cards
				hand1.remove_four()
				print("Player 1 has: ")
				hand1.display()
				rank=0				
				if len(hand1.cards)!=0:
				    while hand1.check(rank):
				        rank = int(input("Please choose a card rank you would like to ask the other player if they have (between 1-13): "))
			
			if len(deck.cards) != 0:
				print("Player 1 draw one card from the deck ...")
				c1=hand1.draw(deck,rank)
			if c1:
				break


	# if Player 2's turn
		while turn == 1:
		    hand2.remove_four()
		    rank=0			
		    if len(hand2.cards)!=0:
		        while hand2.check(rank):
			        rank = int(input("Please choose a card rank you would like to ask the other player if they have (between 1-13): "))				    
					
		    while hand2.go_fish(hand1,rank):
			    # remomve 4 same cards
			    hand2.remove_four()
			    print("Player 2 has: ")
			    hand2.display()
			    rank=0				
			    if len(hand2.cards) != 0:
			        while hand2.check(rank):
			            rank = int(input("Please choose a card rank you would like to ask the other player if they have (between 1-13): "))
			
		    # draw from deck
		    if len(deck.cards) != 0:
			    print("Player 2 draw one card from the deck ...")
			    c2 = hand2.draw(deck,rank)
		    if c2:
			    break
		
		# Result
		print("Player1 Score: "+str(hand1.score))
		print("Player2 Score: "+str(hand2.score))
		# change turn
		turn = turn * -1
	if hand1.score > hand2.score:
		print("Player1 wins")
	elif hand1.score < hand2.score:
		print("Player2 wins")
	else:
		print("Draw")


#Start game
start_game()



