#include <array>
#include <type_traits>

// Usually given an std::array<T, N> and a C-style array T[N]
// sizeof(std::array<T,N>) == sizeof(T[N]) but it's not ensured
// so this static_assert checks that it's indeed the case and if not
// gives a compilation error
void check_types_size() {
    [[maybe_unused]]
    std::array<int, 3> a;
    int b[3];

    // Check that the sizeof the std::array equals the size of a C-style array
    static_assert(sizeof(b) == sizeof(b));
}
