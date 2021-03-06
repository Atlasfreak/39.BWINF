﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.IO;

namespace Bwinf_Aufgabe1
{
	class Program
	{
		static void Main(string[] args)
		{
			List<List<string>> temp;
			string[] wordsToFind;
			string[] availableWords;
			Dictionary<string, string> allWords = new Dictionary<string, string>();
			string result = string.Empty;
			string originalString = string.Empty;
			string filename = string.Empty;

			if (args.Length == 0)
			{
				filename = GetFilename();
			}
			else
			{
				filename = args[0];
			}

			while (true)
			{
				//Input
				temp = ReadFromFile(filename);
				originalString = temp[0][0];
				wordsToFind = temp[1].ToArray();
				availableWords = temp[2].ToArray();

				Console.WriteLine($"Originaler Satz:\n{originalString}\n");

				//maximale Wortlänge herausfinden
				int maxLength = availableWords.OrderBy(word => word.Length).Last().Length;

				//über jede mögliche Wortlänge iterieren
				for (int wordLength = 1; wordLength <= maxLength; wordLength++)
				{
					//Wenn es kein Wort mit der Länge wordLength gibt soll diese nicht beachtet werden
					if (availableWords.Count(word => word.Length == wordLength) > 0)
					{
						//Alle Wörter gleicher Länge zusammenfassen
						string[] currentAvailableWords = availableWords.Where(word => word.Length == wordLength).ToArray();
						string[] currentWordsToFind = wordsToFind.Where(word => word.Length == wordLength).ToArray();
						//Kopien der Listen erstellen aus denen man Elemente entfernen kann ohne dass es zu Index Problemen kommt
						List<string> notUsedWords = new List<string>();
						List<string> notUsedUnfinishedWords = new List<string>();
						notUsedWords.AddRange(currentAvailableWords);
						notUsedUnfinishedWords.AddRange(currentWordsToFind);

						bool finished = false;
						while (!finished)
						{
							for (int i = 0; i < currentWordsToFind.Length; i++)
							{
								if (notUsedUnfinishedWords.Contains(currentWordsToFind[i]))
								{
									List<string> wordsThatFit = WordsThatFit(currentWordsToFind[i], notUsedWords);
									//Wenn nur ein Wort passt kann dieses direkt eingesetzt werden
									if (wordsThatFit.Count == 1)
									{
										notUsedWords.Remove(wordsThatFit[0]);
										notUsedUnfinishedWords.Remove(currentWordsToFind[i]);
										if (!allWords.ContainsKey(currentWordsToFind[i]))
											allWords.Add(currentWordsToFind[i], wordsThatFit[0]);
									}
								}

								if (notUsedUnfinishedWords.Count == 0)
								{
									finished = true;
									break;
								}
							}
						}
					}
				}
				//Zusammenbauen vom Output string
				foreach (string word in wordsToFind)
				{
					result += $"{allWords[word]} ";
				}
				//Einfügen von Sonderzeichen falls vorhanden
				for (int i = 0; i < originalString.Length; i++)
				{
					if (new char[] { ',', '.', '!' }.Contains(originalString[i]))
					{
						result = result.Insert(i, originalString[i].ToString());
					}
				}
				//Output
				Console.WriteLine($"Ergebnis:\n{result}");
				Console.Write("\nEine beliebige Taste drücken um fortzufahren. . .");
				Console.ReadKey();

				allWords.Clear();
				result = string.Empty;
				filename = GetFilename();
			}
		}

		/// <summary>
		/// Überprüft ob ein vollständiges Wort und ein Wort mit Lücken kompatibel sind
		/// </summary>
		static bool WordsFit(string unfinishedWord, string finishedWord)
		{
			for (int i = 0; i < unfinishedWord.Length; i++)
			{
				if (unfinishedWord[i] != '_' && unfinishedWord[i] != finishedWord[i])
				{
					return false;
				}
			}
			return true;
		}

		/// <summary>
		/// Gibt zurück welche Wörter aus einer Wörterliste in ein Wort mit Lücken passen.
		/// </summary>
		static List<string> WordsThatFit(string unfinishedWord, List<string> possibleWords)
		{
			List<string> wordsFit = new List<string>();
			foreach (string word in possibleWords)
			{
				//Wenn ein Wort passt aber doppelt ist, wird es nicht ein zweites mal berücksichtigt
				if (WordsFit(unfinishedWord, word) && !wordsFit.Contains(word))
				{
					wordsFit.Add(word);
				}
			}
			return wordsFit;
		}

		/// <summary>
		/// Bekommt einen Dateinamen vom Nutzer. Wenn dieser nicht existiert wird erneut nachgefragt.
		/// </summary>
		static string GetFilename()
		{
			string filename = string.Empty;
			while (!File.Exists(filename))
			{
				Console.Clear();
				Console.Write("Dateiname: ");
				filename = Console.ReadLine();
				Console.Clear();
			}

			return filename;
		}

		/// <summary>
		/// Liest eine Datei aus
		/// </summary>
		static List<List<string>> ReadFromFile(string filename)
		{
			string originalString = string.Empty;
			List<List<string>> temp = new List<List<string>>();
			using (StreamReader sr = new StreamReader(filename))
			{
				while (sr.Peek() >= 0)
				{
					if (originalString.Length == 0)
					{
						originalString = sr.ReadLine();
						temp.Add(new List<string>() { originalString });
						temp.Add(Regex.Replace(input: originalString, pattern: @",|!|\.", replacement: "").Split(' ').ToList());
					}
					else
					{
						temp.Add(sr.ReadLine().Split(' ').ToList());
					}
				}
			}
			return temp;
		}
	}
}
