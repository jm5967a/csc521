(ns clojure-quirk.clojure-quirk (:require [instaparse.core :as insta])(:require [clojure.java.io :as io])(:require [clojure.math.numeric-tower :as math])(require [clojure.string :as string]))

(def parse
  (insta/parser
  (slurp(clojure.java.io/resource "quirk.txt")) :auto-whitespace :standard)
  )
(defn zero [x] ;Setup index functions
  (nth x 0))

(defn firstind [x] 
  (nth x 1))

(defn secondind [x]
  (nth x 2))

(defn third [x] ;Setup index functions
  (nth x 3))

(defn fourth [x]
  (nth x 4))

(defn fifth [x] ;Setup index functions
  (nth x 5))
(defn sixth [x]
  (nth x 6))


(defn parint [s] ;Setup function to to turn integers in a string in ints
  (Integer/parseInt (re-find #"\A-?\d+" s)))

(defn call [this & that]  ;function to call other functions by labs
  (apply (resolve (symbol this)) that))

(defn Program [x] ;Establist main interpreter function
  (try   
    (case (zero x) ;Check to see whether the first element of the x is Statement or Program-
      :Statement (call "Statement" (firstind x))
      :Program (
        (doseq [[please work] (map vector  x (range))] ;Creates loop to go through the indexes of the tree 
          (cond
            (= work 0) ()
            (= work 1) (call "Statement" (firstind please))
            :else ((call "Program" (firstind please)) (call "Program" (secondind please)))          
           )))
       ;(call "Program" (firstind please))(call "Program2"(secondind please))))))     
)(catch Exception e)))
(defn Statement [x] ;Function to break down Statement into its' child components
  (cond 
   (=(zero x):FunctionDeclaration)(call "FunctionDeclaration" x)
   (=(zero x):Print)(call "Print" (secondind x))
   (=(zero x):Assignment)(call "Assignment" x)
   )
  )
(defn FunctionDeclaration [x] ;Function 
  (def temp [])
  (def append []) ;Setup vector that will eventually hold all of the elments needed for funcdec
  (let [funcnam (call "namefun" (secondind x))] 
	  (if(=(zero(third x)):LPAREN)
	    (call "FunctionParams" (fourth x)))
	  (if(=(zero(fifth x)):LBRACE) 
	     (def append(conj append temp)))
	  (def append(conj append (sixth x)))
	  (def scope(assoc-in scope ["function" funcnam] append))) ;Append func elments to scope
  )

(defn FunctionParams [x]  ;Break func params down 
  (call "Namelist" (firstind x))
  (do temp)
    )
(defn Namelist [x]
  (try
    (def temp (conj temp (call "namefun" (firstind x)))) ;append results idents in namelist to temp
    (Namelist (third x))
  (catch Exception e
    (do temp) ;Pass temp back 
    ))
  )
(defn Print [x]
    (if(=(zero x):Expression)  
      (let[y(call "Expression"  x)] ;Set local variable, y, to the results of expression
        (println (double(parint(re-find #"-?\d+" y)))) ;Find double in string and print them 
       ))
  )
(defn Functioncall [x]
  (def temps []) ;Establish temp vector that will be used used in various sub functions
  ;<FunctionCall> ->  <Name> LPAREN <FunctionCallParams> COLON <Number> | <Name> LPAREN <FunctionCallParams>
	(let [funccall (call "namefun" (firstind x))]
	    (let [full (get-in scope ["function" funccall])]
	      (let [funcparams (zero full)]
	        (let [code (firstind full)]
	          (let [callparams (call "FunctionCallParams" (third x) funcparams funccall)]
             (try 
               (let [index (call "Value" (fifth x))]
               (do(nth(call "FunctionBody" code)(parint index))))  ;If the function call wants back a specific index then runs this               
              (catch Exception e
                (do(call "FunctionBody" code)))) ;Execute  main function body code
    ))))))
   
;<FunctionCallParams> ->  <ParameterList> RPAREN | RPAREN
(defn FunctionCallParams [x y z]
    (let [params(call "ParameterList" (firstind x))]
      (doseq [[please work] (map vector  y (range))]
      (def scope(assoc-in scope ["running" please] (get params  work))) ;Put function call params in scope vector 
     )
    (do  temps)
  ))
(defn ParameterList [x] 
; <ParameterList> -> <Parameter> COMMA <ParameterList> | <Parameter>
	(try
	  (def temps (conj temps (call "Parameter" (firstind(firstind x))))) 
	  (ParameterList (third x))
	 (catch Exception e
	    (do temps) ;return found parameter veector
	    ))
	  )
;<FunctionBody> -> <Program> <Return> | <Return>
(defn FunctionBody [x] ;Main function body that executes the function code
  (case (zero (firstind x))
    :Program ((Program (firstind x))(call "FunctionBody" (secondind (secondind x))))
    :Return (call "Return" (secondind(firstind x)))
    :Parameter ((def works(call "Return"  x)) (do works))
  )
 )
(defn Return [x] ;Return method in function
  (def temps [])
  (ParameterList  x)
  )
;<Return> -> RETURN <ParameterList>
(defn Parameter [x]
  (case (zero x)
    :Expression (call "Expression" x)
    :Name (call "Value" x)
    )
  )
(defn Expression [x]
  ;<Expression> -> <Term> ADD <Expression> | <Term> SUB <Expression> | <Term>
 (try
   (if(=(zero(firstind x)):Term)(def k (call "Term" (firstind x)))) ;handle first subtraction or addition
   (case (firstind (secondind x))
     "+" ((if(=(zero(firstind(third x))):Term)
            (def t (parint(call "Term" (firstind (third x)))))) (def k (+ (parint k) t)))
     "-" ((if(=(zero (firstind (third x))):Term)
            (def t (parint(call "Term" (firstind (third x)))))) (def k (- (parint k) t)))
    )
  (catch Exception e)) ;If no add or subtract is found
  
 (try
   (case (firstind(secondind(third x)))
     "+" ((if(=(zero(firstind(third(third x))))):Term)
           (def t (parint(call "Term" (firstind(third(third x)))))) (def k (+ k t)))
     "-" ((if(=(zero(firstind(third(third x))))):Term)
           (def t (parint(call "Term" (firstind(third(third x)))))) (def k (- k t)))
      )
  (catch Exception e))
 (try 
   (case (firstind(secondind x))) ;handle third subtraction or addition
     "+" ((if(=(zero(firstind x)):Term)
            (def t (parint(call "Term" (firstind(third x))))) (def k (+ (parint k) t))))
     "-" ((if(=(zero(firstind x)):Term)
            (def t (parint(call "Term" (firstind(third x))))) (def k (- (parint k) t))))
 (catch Exception e ;If no add or subtract is found
   ))
    (str k) 
    )
(def scope {"global" {}}) ;define global scope used for all declarations

(defn Assignment [x] ;Break down assignments into single or multiple
   (case (zero(firstind x))
     :SingleAssignment (call "Single_Assign" (firstind x))
     :MultipleAssignment (call "Multiple_Assign" (firstind x))
      )
   )
(defn Single_Assign [x]
  (if(=(zero(secondind x)):Name)(def n (call "namefun" (secondind x)))) ;get variable nume
  (if(=(zero(fourth x)):Expression)(def value (call "Expression" (fourth x)))) ;get variable value
  (def scope(assoc-in scope ["global" n] value)) ;add pair to scope
  )
(defn Multiple_Assign [x]
  ;<MultipleAssignment> -> VAR <NameList> ASSIGN <FunctionCall>
  (def temp [])
  (let [nam (call "Namelist" (secondind x))]
	  (try
      (call "Functioncall" (fourth x)) 
	  (catch Exception e
	    (doseq [[please work] (map vector  nam (range))]
	       (def scope(assoc-in scope ["global" please] (get works  work))) 
	      ))
	     ))
  )
(defn namefun [x]
  (firstind (firstind x)) 
  )
(defn Term [x] 
    (if(=(zero(firstind x)):Factor)
      (def z(call "Factor" (firstind x))))
    (try
	    (case (zero(secondind x)) ;check for first multi or division and if so perform action
	      :DIV ((if(=(firstind(third x))):Factor)
              (def div (parint(call "Factor" (firstind(third x)))))(def z (/ (parint z) div)))
        :MULT ((if(=(firstind(third x))):Factor)
                (def div (parint(call "Factor" (firstind(third x)))))(def z (* (parint z) div)))
	      )
     (catch Exception e))
    (try
	    (case (zero(secondind(third x))) ;check for second
	      :DIV ((if(=(firstind(third(third x)))):Factor)
              (def div (parint(call "Factor" (firstind(third(third x))))))(def z (/ z div)))
	      :MULT ((if(=(firstind(third(third x)))):Factor)
               (def div (parint(call "Factor" (firstind(third(third x))))))(def z (* z div)))
	      )
	  (catch Exception e))
	  (do z)
  )
(defn Factor [x]
  (try 
    (if(= (zero(secondind x)) :EXP) (call "expon" x))
  (catch Exception e
	  (case (zero(firstind x)) ;check to see what factor needs to break down to 
		  :Value (call "Value" (firstind(firstind x)))
			:SubExpression (if(=(zero(firstind(firstind x))):LPAREN)
                       (call "SubExpression" (secondind (firstind x))))
			:FunctionCall (call "Functioncall" (firstind x))
			   )))
  )
(defn expon [x] 
  (let [exp (parint(call "Value" (firstind(second x))))] ;Grab number that has exponent
	  (let [exp2 (parint(call "Value" (second(second(third x)))))] ;Get exponent
     (let [z (math/expt exp exp2)] ;Perform accion
       (do z)
  ))))
(defn SubExpression [x]
  (call "Expression" x) ;Handle parenthesis around values
  )
(defn Value [x]
  (try 
	  (cond 
	    (=(zero(firstind x)) :SUB) (call "name2" x)  ;check to see if the value has + or - before it 
	    (=(zero(firstind x)):ADD) (call "name2" x)
     :else (
       (case (zero x) ;if not go on breaking it down
			   :Number (call "Num"  x)
				 :Name (call "name1" (firstind(firstind x)))
    )))
  (catch Exception e
    (case (zero x)
      :Number (call "Num"  x)
      :Name (call "name1" (firstind(firstind x)))
      ))))
      
 
(defn name1 [x]
  (try 
    (def t(get-in scope ["running" x]))  ;Get values from scope--Different function depending on what is needed
    (parint t)
  (catch Exception e
     (def t(get-in scope ["global" x]))
    ))
  (do t) 
  )
(defn name2 [x]
  (try 
    (def t(get-in scope ["running" (firstind(secondind x))])) ;Get values from scope
    (parint t)
  (catch Exception e
    (def t(get-in scope ["global" (firstind(secondind x))]))
    ))
  (cond
	  (=(zero(firstind x)):SUB)(do(str(*(parint t)-1)))  ;if operators found before int then apply either -1 for - or abs for +
	  (=(zero(firstind x)):ADD)(do(str(math/abs(parint t))))
   )
  )
(defn Num [x] ;main function for handling numbers
 (cond
   (=(zero(firstind x)):NUMBER)(do(firstind(firstind x)))  
   (=(zero(firstind x)):SUB)(do(str(*(parint (firstind(secondind x)))-1)))
   (=(zero(firstind x)):ADD)(do(str(math/abs(parint (firstind(secondind x))))))
   ) 
  )

(defn -main [& args]
  (def SHOW_PARSE_TREE false)
  (def stdin (slurp *in*)) ;read standard input
  (if (.equals "-pt" (first *command-line-args*)) ;if pt in command line only print parse tree
    (def SHOW_PARSE_TREE true)
  )
  (def quirk-parser (insta/parser (slurp "resources/quirk-grammar-ebnf.txt") :auto-whitespace :standard)) ;initialize instaparse
  (def parse-tree (quirk-parser stdin)) 
   (if (= true SHOW_PARSE_TREE) 
    (println parse-tree) 
    (Program parse-tree))
  (println "done!")
  (System/exit 0)
 )
(-main)