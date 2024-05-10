! ############# XARXES COMPLEXES ################
! ############### ASSIGNMENT 1 ###################
! ############## ALBERT PLAZAS ###################

PROGRAM xarxes_assignment_1
    implicit none
    integer :: N, E, nlineas, ios, i, j
    real :: k
    integer, dimension(:), allocatable :: V, conexions
    integer, dimension(:), allocatable :: D
    character(len=100) :: filename

    ! Lee el nombre del archivo desde los argumentos de línea de comandos
    call getarg(1, filename)

    ! Lee el numero de lineas que hay e un achivo
    open(unit=10, file=filename, status='old')
    nlineas = 0
    do while(.true.)
        read(10,*,iostat=ios) 
        if(ios/=0) then ! Iostat=0 significa que se ha leido correctamente, si no, salimos del bucle
            exit
        end if
        nlineas = nlineas + 1
    end do
    close(10)
    print*, 'Number of lines: ', nlineas

    ! Allocate la memoria para vector V
    allocate(V(nlineas)) ! Vector de nodos
    allocate(conexions(nlineas)) ! Vector de conexiones

    ! Lee los datos del archivo y los guarda en los vectores V y conexions
    open(unit=10, file=filename, status='old')
    do i=1, nlineas
        read(10,*) V(i), conexions(i)
    end do
    close(10)

    ! Calcula el numero de nodos
    N = maxval(V) - V(1) + 1 ! Añadimos 1 porque los nodos empiezan en 0
    print*, 'Number of nodes: ', N

    ! Allocate la memoria para vector D
    allocate(D(N)) ! Vector de grados

    ! Inicializa el vector D
    D = 0 
    j = 1 ! Inicializa el contador de nodos
    D(1) = 1 ! Inicializa el primer nodo
    ! Calcula el grado de cada nodo
    do i=1, nlineas
        if (V(i) .eq. V(i+1)) then ! Si el nodo es el mismo que el siguiente
            D(j) = D(j) + 1 ! Incrementa el grado del nodo
        end if
        if (V(i) .ne. V(i+1)) then ! Si el nodo es diferente al siguiente
            j = j + 1 ! Incrementa el contador de nodos
            D(j) = 1 ! Inicializa el grado del nuevo nodo
        end if
    end do

    if (V(nlineas) .ne. V(nlineas-1)) then ! Si el ultimo nodo es diferente al penultimo
        D(N) = 1 ! Inicializa el grado del ultimo nodo
    end if

    ! Resultados
    E = int(sum(D) * 0.5) ! El numero de aristas es la mitad de la suma de los grados
    print*, 'Number of edges: ', E 
    k = real(E)*2 / real(N) ! El grado medio es el doble del numero de aristas entre el numero de nodos
    print*, 'Average degree <k>: ', k

    ! Libera la memoria
    deallocate(V)
    deallocate(conexions)
    deallocate(D)

END PROGRAM xarxes_assignment_1