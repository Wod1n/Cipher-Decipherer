# Python Decypher

import numpy as np
import matplotlib.pyplot as plt

import string
import random
import copy

def generate_cipher(dictionary = True):
    alphabet = list(string.ascii_lowercase)
    substitution = list(string.ascii_lowercase)

    random.shuffle(substitution)

    if not dictionary:
        return substitution

    cipher = {}

    for k, v in zip(alphabet, substitution):
        cipher[k] = v

    return cipher

def generate_probabilities():

    character_order = np.ones((26,26))
    character_count = np.zeros(26)

    f = open("moby_dick.txt", "r")
    content = f.read()
    f.close()
    index = -1
    for line in content:
        line = line.rstrip()
        old_index = index
        index = -1
        if line in list(string.ascii_lowercase):
            index = ord(line) - 97
            character_count[index] += 1
        if line in list(string.ascii_uppercase):
            index = ord(line) - 65
            character_count[index] += 1

        if index != -1 and old_index != -1:
            character_order[old_index][index] += 1
            coord = [old_index, index]

    i = 0
    while i < len(character_count):
        j = 0
        while j < len(character_order[i]):
            character_order[i][j] = np.log(character_order[i][j])
            character_order[i][j] -= np.log(character_count[i] + 26)
            j += 1
        i += 1

    return character_order

def encrypt_message(cipher):
    f = open("message.txt", "r")
    content = f.read()
    f.close()

    content = content.replace("\n"," ")
    content = content.lower()

    encrypted_message = ""
    i = 0
    while i < len(content):
        if content[i] in list(string.ascii_lowercase):
            encrypted_message += cipher[content[i]]
        else:
            encrypted_message += content[i]
        i += 1

    return encrypted_message

def decrypt_message(cipher, encrypted_message):
    decrypted_message = ""

    if isinstance(cipher, list):
        cipher_list = copy.copy(cipher)
        cipher = {}
        alphabet = list(string.ascii_lowercase)
        for k,v in zip(alphabet, cipher_list):
            cipher[k] = v

    i = 0
    while i < len(encrypted_message):
        if encrypted_message[i] in list(string.ascii_lowercase):
            decrypted_message += cipher[encrypted_message[i]]

        else:
            decrypted_message += encrypted_message[i]
        i += 1

    return decrypted_message

def solution_test(trial):
    character_order = np.ones((26,26))
    character_count = np.zeros(26)
    index = -1
    for character in trial:
            old_index = index
            index = -1
            if character in list(string.ascii_lowercase):
                index = ord(character) - 97
                character_count[index] += 1
            if index != -1 and old_index != -1:
                character_order[old_index][index] += 1
                coord = [old_index, index]

    i = 0
    while i < len(character_count):
        j = 0
        while j < len(character_order[i]):
            character_order[i][j] = np.log(character_order[i][j])
            character_order[i][j] -= np.log(character_count[i] + 26)
            j += 1
        i += 1

    score = 0
    k = 0
    while k < len(character_count):
        l = 0
        while l < len(character_order[k]):
            probability_difference = character_order[k][l] - sample_probability[k][l]
            if probability_difference < 0:
                score -= probability_difference
            else:
                score += probability_difference
            l += 1
        k += 1

    return score

def randomise_ciphers(cipher_pool, additional):
    initial_number = len(cipher_pool)
    i = 0
    while i < initial_number:
        j = 0
        while j < additional:
            position1 = random.randint(0,25)
            position2 = random.randint(0,25)
            position_swaps = [position1, position2]
            new_cipher = copy.copy(cipher_pool[i])
            new_cipher[position1], new_cipher[position2] = new_cipher[position2], new_cipher[position1]
            cipher_pool.append(new_cipher)
            j += 1
        i += 1

    return cipher_pool

def sort_scores(cipher_pool):
    score_sheet = []
    j = 0
    while j < len(cipher_pool):
        trial_decryption = decrypt_message(cipher_pool[j], encrypted_message)
        score = solution_test(trial_decryption)
        k = 0
        while k < len(score_sheet)-1:
            if k == 0 and score < score_sheet[k][0]:
                score_sheet.insert(k, [score,j])
                break
            if score > score_sheet[k][0] and score < score_sheet[k+1][0]:
                score_sheet.insert(k+1, [score, j])
                break
            k += 1
        if k == len(score_sheet) or k == len(score_sheet)-1:
            score_sheet.append([score, j])
        j += 1

    kept_ciphers = []

    l = 0
    while l < 5:
        kept_ciphers.append(cipher_pool[score_sheet[l][1]])
        l += 1

    return kept_ciphers

def optimise_solution(cipher_pool):
    k = 0
    old_score = 0
    while True:
        cipher_pool = randomise_ciphers(cipher_pool, additional)
        cipher_pool = sort_scores(cipher_pool)
        current_score = solution_test(decrypt_message(cipher_pool[0], encrypted_message))
        print(current_score)
        if current_score == old_score:
            k += 1
        if current_score != old_score:
            k = 0
        if k == 200:
            return cipher_pool
        old_score = current_score

cipher_to_find = generate_cipher()

encrypted_message = encrypt_message(cipher_to_find)
sample_probability = generate_probabilities()

additional = 5
generate_initial = 5

cipher_pool = []
i = 0
while i < generate_initial:
    cipher_pool.append(generate_cipher(False))
    i += 1

cipher_pool = optimise_solution(cipher_pool)

print(decrypt_message(cipher_pool[0], encrypted_message))
