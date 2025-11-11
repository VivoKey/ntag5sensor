//
// The goal of uncompress is to arrive at a 16-bit value, when the input is a
// single byte of information.
//
// The approach taken here is to reuse the floating point concept, but apply it
// to this. Just as it is possible to store relatively large numbers using an
// IEEE 754 representation of a 32 bit value, we make use of a similar concept.
//
// In IEEE 754 representation, there consists of concept of a signed exponent,
// and a signed significand. The signed exponent allows representation of
// values between 2^127 to 2^-128. The signficand is also signed.
//
// The term 'significand' is the integer bit plus the fraction. The 'fraction'
// is the fractional part of the significand.
//
// IEEE Single Precision Format
//
// | b31 | b30 to b23 | bit22 to bit0 |
// | Sign | Signed Exponent | Fraction |
//
// In what we need, we do not need signed exponents nor do we need signed
// significands. So, we use an unsigned exponent representation and an unsigned
// significand.
//
// uncompress takes an input byte and interprets the first 4 bits as an
// exponent, and the last 4 bits as a fraction, with an implicit integer bit
//
// The mathematical representation is similar to the concept for floating point
// numbers. First off, the bit field 7:4 is the Exponent, and the bit field 3:0
// is the fractional part of the significand.
//
//
// | b7 b6 b5 b4 | b3 b2 b1 b0 |
// | unsigned | |
// | Exponent | Fraction |
//
// The number representation is:
//
// ( 2 ^ Exponent ) * 1.Fraction
//
// Note the 'implicit integer bit'. Normally, the hidden integer is 1. However,
// there is an exception. If the Exponent is zero, the representation
// becomes the following:
//
// ( 2 ^ 0 ) * 0.Fraction
//
// This is the concept called the 'denormalized number' identical to the IEEE
// 754 representation of floating point numbers. Concept isn't new... this
// allows us to represent the value 0.
//
// Let's go through one example...
//
// Let's say input is 0x9A.
//
// Exponent = 9
// Fraction = A
//
// Since the Exponent is non-zero, the number representation is:
//
// 2 ^ 9 * (1.1010)
//
// So, we take 1.1010 and shift left by 9 positions. It is best illustrated in
// binary...
//
// 1.1010 << 9 = 1 1010 00000 = 0x340
//
// The main advantage is that it allows a very large range dynamic range
// to be represented in 8 bits. The largest number that can be represented
// is 0xFF, and this translates to:
//
// 2 ^ 15 * 1.1111
//
// 1.1111 << 15 = 1111 1000 0000 0000 = 0xF800
//
// When the exponent is less than 4, notice that the fraction bits are
// truncated. What this means is that there can be multiple ways of getting an
// output from 0 to
// the value '0x0000' to 0x000F
//
// To illustrate the case where exponents are less than 4:
// Input Output
// 00 0000
// 02 0000
// 08 0001
// 0A 0001
// 10 0002
// 14 0002
// 18 0003
// 1A 0003
// 20 0004
// 24 0005
// 28 0006
// 2c 0007
// 30 0008
// 32 0009
// 34 000a
// 36 000b
// 38 000c
// 3c 000e
// 3e 000f
//
// At exponent of 4 or greater, the fraction bits are no longer being thrown
// away, so, we now have linear values
// 40 0010
// 41 0011
// 42 0012
// 43 0013
// 44 0014
//
// But alas, once the exponent is greater than 4, we now stuff the lower
// fractional bits with zero, and we begin to skip numbers...
// 50 0020
// 51 0022
// 52 0024
// 53 0026
// 54 0028
//
// Well...strictly speaking, the IEEE format treats the largest possible
// exponent as 'infinity' or NAN. Let's not go there... Denorm concept is useful
// for us since it allows us to represent zero. However, infinity or NAN
// concepts are not useful for us.
//

/***************************************************************************/
uint16_t Uncompress(uint8_t input) // It is important for the input to be
 // unsigned 8-bit.
{
    uint16_t output = 0;
    uint8_t exponent = 0;

    // Handle denorm case where exponent is zero. In this case, we are
    // evaluating the value with the integer bit is zero (0.F). So, we round up
    // if the fraction represents a value of 1/2 or greater. Since the fraction
    // is 4 bits, an input of less than 8/16 is less than half. If less than
    // half, return zero. Otherwise, we know that we will return a 1 later.
    //
    if( input < 8 ) return 0;

    //
    // At this point, the exponent is non-zero, so, put in the implicit
    // fraction. Note that when we get the input, it comes in already shifted
    // by 4. So, we are dealing with a value already 4 times larger than the
    // actual starting point.
    //
    // Never fear... we just make an adjustment to the exponent and shift
    // left/right accordingly. The result will be the same as the floating
    // point concept described above.
    //

    exponent = (input & 0xF0 ) >> 4; // extracts the exponent
    output = 0x10 | (input & 0x0F); // extracts the fraction and adds
    // in the implicit integer

    if( exponent >= 4 ) return ( output << (exponent-4) );
    return( output >> (4-exponent) );
}


// --------------------------------------------------------------------
// What if someone wants to do the inverse function?
//
// Let's say we want to figure out what byte value best represents the number
// of 32 KHz timer ticks for 500 ms.
//
// We start of by knowing how many 32 KHz cycles are in that given time period.
// Let's say that we want to have the RTC wake up every 500 ms.
//
// 500 ms * 32 KHz = 16000 cycles
//
// Then, we take the calculator, and find out what 64 looks like from a binary
// value viewpoint. Using a hex calculator, we see that:
//
// 16000 = 11111010000000
//
// ... in floating point representation...
//
// = 11111010000000.00000
//
// The next step is to normalize the value. Normalizing the value means that
// we represent the value in 1.F format. We do this by moving the decimal value
// left until we get the 1.F representation. The number of times we move the
// decimal point left is the exponent. Since we need to move the decimal point
// left before we get to the 1.F represenation...
//
// 16000 = 2^13 * 1.1111010000000
//
// The exponent is therefore 13, and the digits to the right hand side of the
// decimal point is the fraction. What we need is the the first four fractional
// bits. The first four fraction bits is 1111. We truncate the rest,
// unfortunately.
//
// Therefore, the nearest byte representation for 500 ms is 0xDF
//
// Notice that if you plugged in 0xDF into this uncompress function, you will
// get 496 ms. The reason we didn't quite get 500 ms is that we had to throw
// away the 6th fractional bit.
//
// Anyway, this leads us to the following function. This function takes in a
// 16-bit value and compresses it.

/***************************************************************************/
uint8_t Compress(uint16_t input) // input should be a 16-bit unsigned value
{
    uint32_t tmp = 0;
    uint32_t exponent = 0;
    uint32_t significand = 0;

    if(input==0)
    return 0;


    // handle denorm cases
    // There are multiple answers to 0x0000 and 0x0001 input due to rounding
    // error introduced throught the gradual underflow
    // Answer for 0x0000 is from 0x00 to 0x07
    // Answer for 0x0001 is from 0x08 to 0x0F
    // We will just 'pick one' answer.
    if(input == 0x0000) return 0x00;
    if(input == 0x0001) return 0x08;

    // Now we have the denorm cases out of the way, the exponent should be at
    // least one at this point.
    exponent = 0;
    tmp = input;
    while(1)
    {
        tmp >>= 1; // Shift until there is only the integer in the lease
        // significant position
        exponent += 1;
        if(tmp == 1)
        {
        break; // the integer bit has been found. Stop.
        }
    }

    // Once exponent is found, look for the four fractional bits.
    //
    // If the exponent is between 1 to 4, we do not need to do any kind of
    // fractional rounding. Take care of those cases first

    if(exponent < 5) // shift left to align the significant and return the
    // result
    {
        significand = ( input << (4 - exponent) ) ;
        return ( (exponent << 4) | (significand & 0xF));
    }

    // At this point, we need to calculate the fraction.
    //
    // Easiest way is to align the value so that we have the integer and
    // fraction bits at a known bit position.
    //
    // We then round the signficand to the nearest four fractional bits. To do
    // so, it is best that we also look at the 5th fractional bit and update
    // the 4th fractional bit as necessary. During rounding, it is possible for
    // a carry to occur. If this happens, simply add one to the exponent, and
    // shift the signficand by one to get to the same bit positioning.

    significand = input >> (exponent - 5);

    //
    // After the shift, the significand looks like this since we shift the
    // value by 5 less than the exponent. This is what we expect at this point:
    //
    // bit[15:6] bit5 bit4 bit3 bit2 bit1 bit0
    //
    // zeroes 1 2^-1 2^-2 2^-3 2^-4 2^-5
    //
    // ^ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^
    // int fraction
    //

    if(significand & 1) // Check if we need to round up
    {
        significand += 2; // Increment the 4th fraction (in bit1 position)

        // We then check if a carry occurred due to the addition. If a carry
        // did occur, it would have bumped up the number such that bit6 would
        // be set. Bit6 is 0x0040.
        if(significand & 0x0040) // Check for a carry
        {
            exponent += 1; // A carry occurred. Increment the exponent
            significand >>= 1; // shift the signficand right by one
        }
    }

    // Rounding is done... Encode value and return.
    return ( (exponent << 4) | ( (significand >> 1) & 0xF ) );
}