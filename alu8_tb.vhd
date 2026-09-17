use std.textio.all;

entity alu8_tb is
end entity alu8_tb;

architecture sim of alu8_tb is

  component alu8
    port (
      a      : in  bit_vector(7 downto 0);
      b      : in  bit_vector(7 downto 0);
      opcode : in  bit_vector(2 downto 0);
      result : out bit_vector(7 downto 0);
      carry  : out bit
    );
  end component;

  signal a, b, result : bit_vector(7 downto 0);
  signal opcode        : bit_vector(2 downto 0);
  signal carry         : bit;

  file infile  : text open read_mode  is "vectors.txt";
  file outfile : text open write_mode is "dut_results.txt";

begin

  dut: alu8 port map (a => a, b => b, opcode => opcode, result => result, carry => carry);

  process
    variable inline  : line;
    variable outline : line;
    variable v_op    : bit_vector(2 downto 0);
    variable v_a     : bit_vector(7 downto 0);
    variable v_b     : bit_vector(7 downto 0);
  begin
    while not endfile(infile) loop
      readline(infile, inline);
      read(inline, v_op);
      read(inline, v_a);
      read(inline, v_b);

      opcode <= v_op;
      a      <= v_a;
      b      <= v_b;
      wait for 1 ns;

      write(outline, v_op);
      write(outline, string'(" "));
      write(outline, v_a);
      write(outline, string'(" "));
      write(outline, v_b);
      write(outline, string'(" "));
      write(outline, result);
      write(outline, string'(" "));
      write(outline, carry);
      writeline(outfile, outline);
    end loop;
    wait;
  end process;

end architecture sim;
