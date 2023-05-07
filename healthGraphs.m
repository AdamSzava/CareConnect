Array=csvread('testing.csv');
col1 = Array(:, 1);
col2 = Array(:, 2);
plot(col1, col2)
axis equal
grid