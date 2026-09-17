library ieee;
use ieee.numeric_bit.all;

entity alu8 is
  port (
    a      : in  bit_vector(7 downto 0);
    b      : in  bit_vector(7 downto 0);
    opcode : in  bit_vector(2 downto 0);
    result : out bit_vector(7 downto 0);
    carry  : out bit
  );
end entity alu8;

architecture rtl of alu8 is
begin
  process(a, b, opcode)
    variable ua, ub  : unsigned(7 downto 0);
    variable sum9    : unsigned(8 downto 0);
    variable diff9   : signed(8 downto 0);
  begin
    ua := unsigned(a);
    ub := unsigned(b);

    case opcode is
      when "000" =>                      -- ADD
        sum9   := ('0' & ua) + ('0' & ub);
        result <= bit_vector(sum9(7 downto 0));
        carry  <= sum9(8);

      when "001" =>                      -- SUB
        diff9  := signed('0' & ua) - signed('0' & ub);
        result <= bit_vector(diff9(7 downto 0));
        carry  <= diff9(8);              -- borrow

      when "010" =>                      -- AND
        result <= a and b;
        carry  <= '0';

      when "011" =>                      -- OR
        result <= a or b;
        carry  <= '0';

      when "100" =>                      -- XOR
        result <= a xor b;
        carry  <= '0';

      when "101" =>                      -- SHL (logical, shift by 1)
        result <= a(6 downto 0) & '0';
        carry  <= a(7);

      when "110" =>                      -- SHR (logical, shift by 1)
        result <= '0' & a(7 downto 1);
        carry  <= a(0);

      when "111" =>                      -- SRA (arithmetic, shift by 1)
        result <= a(7) & a(7 downto 1);  -- FIX: sign-extend with a(7)
        carry  <= a(0);

      when others =>
        result <= (others => '0');
        carry  <= '0';
    end case;
  end process;
end architecture rtl;
