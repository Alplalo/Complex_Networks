# -------------------------------------
# -- SCRIPT GNUPLOT XARXES COMPLEXES --
# -------------------------------------
# ---------- ALBERT PLAZAS ------------

# ------------- AXIS ------------------

set xlabel 'log k'
#set xlabel 'E/N'
#set ylabel 'U(T)/N'
#set ylabel 'S(T)/N'
#set ylabel 'F(T)/N'
#set ylabel 'C(T)/N'
set ylabel 'log P(k)'

#set xrange [-12:0]
#set yrange [:]

# 

set logscale x
set logscale y

set format x "10^{%L}"
set format y "10^{%L}"

# ---------- LINE STYLE ---------------

set style line 1 lc rgb 'black' lt 1 lw 2
set style line 2 lc rgb 'gray40' lt 1 lw 2
set style line 3 lc rgb 'gray70' lt 1 lw 2

# ------------- TICK LABELS ------------
#set xtics 0.2
#set ytics 2
set mxtics 5
set mytics 5

# ------------- OUTPUT ----------------
set term png
set output 'degree_distribution_gnuplot.png'

#set term postscript enhanced color
#set output 'nom.eps'

# ------------- PLOT ------------------

# ---------- Degree Distribution --------------
plot 'degree_distribution.dat' u 1:($2) w l ls 1 t 'log P(k)'

# ------------- Cumulative Degree Distr ----------------
#plot 'cumulative_degree_distribution.dat' u 1:($2) w l ls 1 t 'logP(ki<=k)'



