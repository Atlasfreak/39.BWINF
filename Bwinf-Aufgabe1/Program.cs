using System;
using System.Collections.Generic;
using System.Linq;
using System.Text.RegularExpressions;
using System.IO;
using System.Text;
using System.Threading.Tasks;

namespace Bwinf_Aufgabe1
{
	class Program
	{
		static void Main(string[] args)
		{
			List<List<string>> temp;
			List<string> wordsToFind = new List<string>();
			List<string> availableWords = new List<string>();
			Dictionary<string, string> allWords = new Dictionary<string, string>();
			string result = string.Empty;
			string originalString = string.Empty;
			string filename = string.Empty;

			if (args.Length == 0)
			{
				while (!File.Exists(filename))
				{
					filename = GetFilename();
				}
			}
			else
			{
				filename = args[0];
			}

			while (true)
			{
				temp = ReadFromFile(filename);
				originalString = temp[0][0];
				wordsToFind = temp[1];
				availableWords = temp[2];

				int maxLength = availableWords.OrderByDescending(word => word.Length).First().Length;

				for (int wordLength = 1; wordLength <= maxLength; wordLength++)
				{
					if (availableWords.Find(x => x.Length == wordLength) != null)
					{
						//Alle Wörter gleicher Länge zusammenfassen
						List<string> currentAvailableWords = availableWords.Where(word => word.Length == wordLength).ToList();
						List<string> currentWordsToFind = wordsToFind.Where(word => word.Length == wordLength).ToList();
						List<string> notUsedWords = new List<string>();
						List<string> notUsedUnfinishedWords = new List<string>();

						notUsedWords.AddRange(currentAvailableWords);
						notUsedUnfinishedWords.AddRange(currentWordsToFind);
						bool finished = false;
						while (!finished)
						{
							for (int i = 0; i < currentWordsToFind.Count; i++)
							{
								if (notUsedUnfinishedWords.Contains(currentWordsToFind[i]))
								{
									List<string> wordsThatFit = WordsThatFit(currentWordsToFind[i], notUsedWords);
									if (wordsThatFit.Count == 1)
									{
										notUsedWords.Remove(wordsThatFit[0]);
										notUsedUnfinishedWords.Remove(currentWordsToFind[i]);
										if (!allWords.ContainsKey(currentWordsToFind[i]))
											allWords.Add(currentWordsToFind[i], wordsThatFit[0]);
									}
								}
							}
							if (notUsedUnfinishedWords.Count == 0)
							{
								finished = true;
							}
						}
					}
				}
				foreach (string word in wordsToFind)
				{
					result += $"{allWords[word]} ";
				}
				for (int i = 0; i < originalString.Length; i++)
				{
					if (new char[] { ',', '.', '!' }.Contains(originalString[i]))
					{
						result = result.Insert(i, originalString[i].ToString());
					}
				}
				Console.WriteLine(result);
				Console.Write("Press any key to continue. . .");
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
				if (unfinishedWord[i] != '_')
				{
					if (unfinishedWord[i] != finishedWord[i])
					{
						return false;
					}
				}
			}
			return true;
		}

		/// <summary>
		/// Gibt zurück welche Wörter aus einer Wörterliste in ein Wort mit Lücken passen. Doppelte Wörter werden nur einfach berücksichtigt
		/// </summary>
		static List<string> WordsThatFit(string unfinishedWord, List<string> possibleWords)
		{
			List<string> wordsFit = new List<string>();
			foreach (string word in possibleWords)
			{
				if (WordsFit(unfinishedWord, word) && !wordsFit.Contains(word))
				{
					wordsFit.Add(word);
				}
			}
			return wordsFit;
		}

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
