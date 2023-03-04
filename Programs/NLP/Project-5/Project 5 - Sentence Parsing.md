## Project 5 - Sentence Parsing

**Sentence** 

The lonely spaceman drifted through the cold dark void in his metal shuttle.

**PSG Tree**

![image-20230304104547893](C:\Users\myaku\AppData\Roaming\Typora\typora-user-images\image-20230304104547893.png)

Phrase Definitions:

S - Simple declarative clause

NP - Noun Phrase

DT - Determiner

JJ - Adjective

NN - Noun, Singular or Mass

VBD - Verb, Past Tense

VP - Verb Phrase

PP - Prepositional Phrase

IN - Preposition or Subordinating Conjunction

PRP - Person Pronoun

**Dependency Parse**

![image-20230304104601262](C:\Users\myaku\AppData\Roaming\Typora\typora-user-images\image-20230304104601262.png)

Relations

The sentence is broken up into two main chunks, "the lonely spaceman" and "drifted through the cold dark void in his metal shuttle". The first is talking about the actor and his description, and the second is the setting and descriptor. Drifted is the action that separates the two chunks. Within the second chunk, it's split into sub chunks that contain the focus on the void and shuttle which are connected together to support "drifted". 

**SRL Parse**

Predicate: 

- Drifted

Arguments: 

- Arg1 - The Lonely Spaceman
- Arg2 - Through the cold dark void in his metal shuttle

Modifiers: 

- Arg2 - DIR
  - Motion along a path

**Pros & Cons**

PSG organizes the sentence in a hierarchy of phrases and definitions. This form of parsing is great at showing how each word stems from different groupings and to the sentence as a whole. The downside of this parse is they are often trained on large data samples and only show phrase definitions. The Dependency Parse builds an acyclic graph based on the predicated (drifted in this sentence) and how words stem in relation to it. In comparison to PSG this is better at showing how components of a sentence effect and depend on other parts focused on a predicate, the downside is that because it's structured around a predicate it can less effective for certain sentences than other parsing and tends to have more components. SRL is a very simple form of parsing which labels components as arguments, predicates, and has modifiers to denote special functions. This is very good for a simple overview of how sentences are structured, but because of its simplicity it doesn't provide as much functionality as other parsers. 