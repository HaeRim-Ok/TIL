# JavaScript

> 학습사이트 : https://www.w3schools.com/js/DEFAULT.asp

### 함수 정의하는 방법

- 함수 선언문 (Function Statement)
- 함수 표현식 (Function Expression)
- Function() 생성자 함수



### 1. 함수 선언문 방식

함수 선언

```js
function add(x,y) {return x+y;}
키워드	   이름(param) 함수 본문 
```



함수 호출

```js
var val = add(3,4);
console.log(val);
```



### 2. 함수 표현식 방식

함수 리터럴로 함수 생성 > 함수를 변수에 할당<br>
JavaScript에서는 함수도 하나의 값으로 취급

함수 선언

```js
var x = 1;	//x 변수에 1을 할당
var y = 2;	//y 변수에 2를 할당
var add = function (x,y) {	//add 변수에 매개변수로 전달되는 두 수를 더한 값을 반환하는 익명 함수 할당
	return x+y;
}
```

```js
var z = x;	
var sum = add;	//변수처럼 다른 변수에 재할당 가능
```



함수 호출

```js
console.log(x);	//1
console.log(add(3,4));	//7

console.log(z);	//1
console.log(sum(3,4));	//7
```



- 익명 함수 표현식

- 기명 함수 표현식
  - 함수 표현식에서 사용된 함수 이름은 외부 코드에서 접근이 불가능		⇒ #1
  - 함수 내부에서 해당 함수를 재귀적으로 호출할 때 또는 디버깅할 때 사용 	⇒ #2

```js
// #1
console.log(add(3, 4));	// 7
console.log(sum(3, 4));	// sum is not defined
```
```js
// #2
var myfactorial = function factorial(n) {
    if (n <= 1) return 1;
    return n * factorial(n - 1);
}

console.log(myfactorial(5));	// 120
console.log(factorial(5));	// factorial is not defined
```



함수 선언문에서 정의한 함수는 외부에서 호출이 가능하도록, 자바스크립트 엔진에 의해서 **함수 이름과 함수 변수 이름이 동일한 기명 함수 표현식**으로 변경

```js
function add(x, y) { return x + y; }
				⇓
var add = function add(x, y) { return x + y; }
   변수 이름		함수 이름
```



### 3. Function() 생성자 함수  방식

Fuction() 기본 내장 생성자 함수> https://developer.mozilla.org/ko/docs/Web/JavaScript/Reference/Global_Objects/Function

함수 선언문, 함수 표현식 방식도 내부적으로는 Function() 생성자 함수를 이용해서 생성

```js
new Function([arg1[,arg2[, ... ARGn]],] functionBody)

var add = new Function('x', 'y', 'return x + y');
console.log(add(3, 4));	// 7 
```



-----------------

### 함수 호이스팅 (Function Hosting)

함수 선언문 형태로 정의한 함수는 함수의 유효 범위가 코드의 맨 처음부터 시작⇒ 함수를 **정의한 위치와 관계 없이** 호출이 가능

```js
console.log(add(1, 2));	// 3

function add(x, y) {  
    return x + y;
}

console.log(add(3, 4)); // 7
```

함수 호이스팅이 발생하는 원인 ⇒ JavaScript의 변수 생성과 초기화 작업이 분리되어 진행되기 때문

함수 표현식 방식에서는 함수 호이스팅이 발생하지 않는다.

```js
console.log(x);     // undefined

var x = 2;			// 생성+초기화
console.log(x);     // 2

//console.log(y);     // y is not defined

var z;
console.log(z);     // undefined

// console.log(add(1, 2)); // add is not defined -> add is not a function

var add = function(x, y) { 
    return x + y;
};

console.log(add(3, 4)); // 7
```

----------

### 함수 종류

### 1. 콜백 함수 (callback function)

개발자가 명시적으로 코드를 통해 호출하는 함수가 아니고,<br>
개발자는 함수를 등록만 하고, 이벤트가 발생했을 때 또는 특정 시점에 도달했을 때 시스템에서 호출하는 함수

특정 함수의 인자로 넘겨서 코드 내부에서 호출되는 함수

### 2. 즉시 실행 함수 (immediate function)

함수를 정의함과 동시에 바로 실행하는 함수

최초 한 번의 실행을 필요로 함

```js
function add(x, y) {
    console.log(x + y);
}
add(3, 4);	//함수 선언문 형식으로 정의한 함수는 호출 통해서 실행

(function add(x, y) {	//함수 리터럴을 괄호로 둘러싸고
      console.log(x + y);
})(3, 4);				// 함수 실행에 필요한 인자를 전달

(function add(x, y) {
      console.log(x + y);
}(3, 4));


(function (x, y) {	//일반적으로 즉시 실행 함수는 한 번만 호출되므로 익명 함수로 구분
      console.log(x + y);
})(3, 4);
(function (x, y) {
      console.log(x + y);
}(3, 4));
```

JQuery 이벤트 선언

```
(function() { 
	$(document).ready(function() {
		...
	});
}());
```



### 3. 함수를 반환하는 함수

```js
var self = function() {
    console.log("a");
    return function() {
        console.log("b");
    };
};

self();                     // a
console.log("---------");
self = self();              // a
self();                     // b
```



### 4. 내부 함수 (inner function)

```js
function parent() {
    var a = 100;
    var b = 200;

    function child() {
        var b = 300;

        console.log(a, b);  // 100, 300 (부모 함수의 변수 사용)
    }

    child();
}

parent();
child();        // child is not defined (외부에서 직접 호출할 수 없도록 차단)
console.log(a); // a is not defined
```

함수 외부에서 내부 함수를 사용할 경우 -> 내부 함수 반환

```js
function parent() {
    var a = 100;
    var b = 200;

    function child() {
        var b = 300;

        console.log(a, b);  // 100, 300
    }

    child();
}

parent();
child();        // child is not defined
console.log(a); // a is not defined
```

