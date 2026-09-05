clear all;
clc;

s = tf('s');
K_P = 5;

G_1 = 200/s;

% From the reference to the error
G_e = 1/(1 + K_P*G_1);
e_ss = freqresp(G_e,0)

% From d_1 to the error
G_ed_1 = minreal(-G_1/(1 + K_P*G_1));
ed_1_ss = freqresp(G_ed_1,0)

% From d_2 to the error
G_ed_2 = minreal(-1/(1 + K_P*G_1));
ed_2_ss = freqresp(G_ed_2,0)