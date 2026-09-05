clear all;
clc;

s = tf('s');
K_P = 45;

G_1 = 2/(s + 5);
G_2 = 10*(s + 1)/(s^2 + 20);

% From the reference to the error
G_e = 1/(1 + K_P*G_1*G_2);
e_ss = freqresp(G_e,0)

% From d_1 to the error
G_ed_1 = minreal(-G_1*G_2/(1 + K_P*G_1*G_2));
ed_1_ss = freqresp(G_ed_1,0)

% From d_2 to the error
G_ed_2 = minreal(-G_2/(1 + K_P*G_1*G_2));
ed_2_ss = freqresp(G_ed_2,0)
