# Bachelorarbeit: Systematischer Vergleich von Alpha-Beta und Monte Carlo Tree Search Varianten in dem Spiel Yavalath

## Pythonversion und Libraries

- Python 3.6+
- Benötigte Bibliotheken: numpy, matplotlib, pandas, seaborn, jupyter

## Projektstruktur

- `yavalath.py`: Bitboards und Spiellogik
- `mcts.py`: Alle Versionen der Monte Carlo Tree Search
- `alphabeta.py`: Alle Versionen der Alpha-Beta Suche
- `experiments.ipynb`: Hier wurden die Eexperimente aufgeführt und die Daten verarbeitet und geplottet
- data: Ordner in dem die erhobenen Daten gespeichert wurden
- `tests.py`: Mit dieser Datei wurde während der Implemtierung getestet.
- `game.py`: starten von einzelnen Spilen; kann in der commandline mit den Argumenten aus folgender Liste aufgerufen werden:
    - human       (Menschlicher Spieler
    - alphabeta   (Alpha-Beta Suche ohne Iterative Deepening, aber mit Transposition table)
    - ab_iter     (Alpha-Beta Suche mit Iterative Deepening und Transposition table)
    - mcts        (Monte Carlo Tree Search mit General Domain Knowledge)
    - mcts_ab     (MCTS mit Alpha-Beta Suche)
    - mcts_pns    (MCTS mit Proof Number Search)
