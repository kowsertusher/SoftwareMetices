# -*- coding: utf-8 -*-
"""
Created on Thu Oct 17 11:38:38 2019

@author: tushar
"""

import ast
import copy

mdef = '''
class A(object):
    def meth(self):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        pass
class B(A):
    def _thi(self, mo):
        return sum(i for i in range(10) if i - 2 < 5)
    def fib(self, n):
        self.p = 0
        self.A = 0
        g = A()
        g.meth()
        h=0
        __d = h
        f, k = 0
        if n < 2: return 1
        return fib(n - 1) + fib(n - 2)
class C(B):
    def fib(self,A):
        return 34
    def gf(self):
        return 0
    def df(self):
        return 3
    
    '''

def weighted_method_per_class(source):
    pass

def inheritance_tree(source):
    a = ast.parse(mdef)
    all_node = set()
    definitions = [n for n in ast.walk(a) if type(n) == ast.ClassDef]
    #n for n in ast.walk(a) print(n)
    #for node in ast.walk(a):
      #  if 
      #  print(ast.dump(node))
    #print(definitions)
    inheritance_tree = {}
    for i in definitions:
        all_node.update(i.name)
        inheritance_tree[i.name] = []
        #print(i.name)
        for j in i.bases:
            if not j.id== "object": 
                inheritance_tree[i.name].append(j.id)
                #print("    Inherited",j.id)
    return inheritance_tree, all_node, definitions

def depth_of_inheritance_tree_util(tree,counter, max_counter):
    for child in tree:
        counter+=1
        max_counter = depth_of_inheritance_tree(tree, child, counter, max_counter)
        max_counter = max(max_counter, counter)
        counter-=1
        #print(child, max_counter)
    return max_counter
def depth_of_inheritance_tree(tree, node, counter, max_counter):
    for child in tree[node]:
        if not child == None and not child == "":
            counter+=1

            max_counter = depth_of_inheritance_tree(tree, child, counter, max_counter)
            max_counter = max(max_counter, counter)
            #print(max_counter, node)
            counter-=1
    return max_counter
def Number_of_child(tree, all_node):
    child = {}
    for i in all_node:
        child[i] = []
    for node in all_node:
        for parent in tree:
            if node in tree[parent]:
                child[node].append(parent)
    #for parent in child:
     #   print(parent+" has "+str(len(child[parent]))+" child")
    return child
def attr_hiding_factor(astree):
    dec_sum =0.0
    private_sum =0.0
    for class_obj in astree:
        #print("Class Name: ", class_obj.name)
        variable_count = 0
        private_var_count = 0
        class_attr= set()
        class_pr_attr = set()
        for func_obj in class_obj.body:

            for statements in func_obj.body:
                if isinstance(statements,ast.Assign):
                    for variables in statements.targets:
                        if isinstance(variables,ast.Tuple):
                            if isinstance(variables, ast.Attribute):
                                if variables.attr[0] == "_":
                                    class_attr.update(variables.attr)
                                    class_pr_attr.update(variables.attr)
                                else:
                                    class_attr.update(variables.attr)
                            else:
                                for var in variables.elts:
                                    #print(var.id)
                                    variable_count+=1
                                    if var.id[0] == "_":
                                        private_var_count+=1
                        elif isinstance(variables,ast.Name):
                            #print(variables.id)
                            variable_count+=1
                            if variables.id[0] == "_":
                                private_var_count+=1
                        elif isinstance(variables, ast.Attribute):
                            if variables.attr[0] == "_":
                                class_attr.update(variables.attr)
                                class_pr_attr.update(variables.attr)
                            else:
                                class_attr.update(variables.attr)
        variable_count +=len(class_attr)+len(class_pr_attr)
        private_var_count +=len(class_pr_attr)
        dec_sum += variable_count
        private_sum += private_var_count
        if variable_count>0:
            hiding_factor = private_var_count/variable_count
        else:
            hiding_factor = 0
        #print("   Class "+class_obj.name+"'s AHF is", hiding_factor)
    AHF = private_sum/dec_sum
    print("AHF ",AHF)
            
def method_hiding_factor(astree):
    MHF = 0.0
    dec_sum = 0.0
    private_sum = 0.0
    for class_obj in astree:
        #print("Class Name: ", class_obj.name)
        function_count = 0
        private_func_count = 0
        for func_obj in class_obj.body:
            function_count += 1
            if func_obj.name[0] == "_":
                private_func_count += 1
        #hiding_factor = private_func_count/(function_count+private_func_count)
        private_sum += private_func_count
        dec_sum += function_count+private_func_count
        #print("   Class "+class_obj.name+"'s MHF is", hiding_factor)
    MHF = private_sum/dec_sum
    print("MHF ",MHF)
      
def BFS(child_tree, start, visited, all_inherit):
    for child in child_tree[start]:
        if not child in visited:
            visited.append(child)
            for parent in inheritance_tree[child]:
                all_inherit[child]+=all_inherit[parent]
                #print("chlid "+child+" pretnt "+parent)
            #all_inherit[child]+=all_inherit[start]
            BFS(child_tree, child, visited, all_inherit)
        else:
            return

def BFS1(child_tree, start, visited, all_inherit,class_method):
    for child in child_tree[start]:
        if not child in visited:
            visited.append(child)
            for parent in inheritance_tree[child]:
                all_inherit[child]+=class_method[parent]
                #print("chlid "+child+" pretnt "+parent)
            #all_inherit[child]+=all_inherit[start]
            BFS1(child_tree, child, visited, all_inherit,class_method)
        else:
            return     
def descendants_count(child_tree, start, visited, all_inherit,class_method):
    
    for child in child_tree[start]:
        if not child in visited:
            visited.append(child)
            for parent in inheritance_tree[child]:
                all_inherit[parent]+=[child]#class_method[parent]
                #print("chlid "+child+" pretnt "+parent)
            #all_inherit[child]+=all_inherit[start]
            descendants_count(child_tree, child, visited, all_inherit,class_method)
        else:
            return   

def method_inheritance_factor(inheritance_tree, child_tree, astree):
    class_to_method = {}
    for classes in astree:
        all_method = []
        for methods in classes.body:
            all_method.append(methods.name)
        class_to_method[classes.name] = all_method.copy()
    class_inherit_method = copy.deepcopy(class_to_method) 
    
    visited = []
    for node in inheritance_tree:
        if len(inheritance_tree[node]) == 0:
            BFS(child_tree, node, visited, class_inherit_method)
            
    #print(class_inherit_method)
    #print( class_to_method)
    inherit_count = {}
    for node in class_to_method:
        inherit_count[node] = len(set(class_inherit_method[node])-set(class_to_method[node]))
    #print(inherit_count)
    MIF = {}
    for node in class_to_method:
        if not inherit_count[node] == 0:
            MIF[node] =  inherit_count[node]/len(set(class_inherit_method[node]))
        else:
            MIF[node] = 0
    inherit_sum =0.0
    
    for node in inherit_count:
        inherit_sum += inherit_count[node]
    declare_sum = 0.0
    for node in class_inherit_method:
        declare_sum += len(set(class_inherit_method[node]))
    MF = inherit_sum/declare_sum
    print( "MIF ",MF)


def attr_inheritance_factor(inheritance_tree, child_tree, astree):
    class_to_attribute = {}
    for class_obj in astree:
        #print("Class Name: ", class_obj.name)
        variable_count = 0
        private_var_count = 0
        class_attr= set()
        class_pr_attr = set()
        for func_obj in class_obj.body:

            for statements in func_obj.body:
                if isinstance(statements,ast.Assign):
                    for variables in statements.targets:
                        if isinstance(variables,ast.Tuple):
                            if isinstance(variables, ast.Attribute):
                                if variables.attr[0] == "_":
                                    class_attr.update(variables.attr)
                                    class_pr_attr.update(variables.attr)
                                else:
                                    class_attr.update(variables.attr)
                            else:
                                for var in variables.elts:
                                    #print(var.id)
                                    variable_count+=1
                                    if var.id[0] == "_":
                                        private_var_count+=1
                        elif isinstance(variables,ast.Name):
                            #print(variables.id)
                            variable_count+=1
                            if variables.id[0] == "_":
                                private_var_count+=1
                        elif isinstance(variables, ast.Attribute):
                            if variables.attr[0] == "_":
                                class_attr.update(variables.attr)
                                class_pr_attr.update(variables.attr)
                            else:
                                class_attr.update(variables.attr)
        variable =list(class_attr)+list(class_pr_attr)
        class_to_attribute[class_obj.name] = variable
    #print(class_to_attribute)
    class_inherit_attribute = copy.deepcopy(class_to_attribute) 
    
    visited = []
    for node in inheritance_tree:
        if len(inheritance_tree[node]) == 0:
            BFS(child_tree, node, visited, class_inherit_attribute)
            
    #print(class_inherit_attribute)
    #print( class_to_attribute)
    inherit_count = {}
    for node in class_to_attribute:
        inherit_count[node] = len(set(class_inherit_attribute[node])-set(class_to_attribute[node]))
    #print(inherit_count)
    MIF = {}
    for node in class_to_attribute:
        if not inherit_count[node] == 0:
            MIF[node] =  inherit_count[node]/len(set(class_inherit_attribute[node]))
        else:
            MIF[node] = 0
    inherit_sum =0.0
    
    for node in inherit_count:
        inherit_sum += inherit_count[node]
    declare_sum = 0.0
    for node in class_inherit_attribute:
        declare_sum += len(set(class_inherit_attribute[node]))
    AIF = inherit_sum/declare_sum
    print( "AIF ",AIF)
        
        
    


def polymorphism_factor(inheritance_tree, child_tree, astree):
    class_to_method = {}
    for classes in astree:
        all_method = []
        for methods in classes.body:
            all_method.append(methods.name)
        class_to_method[classes.name] = all_method.copy()
    class_inherit_method = copy.deepcopy(class_to_method) 
    new_class_inherit_method = dict()
    descendants = dict()
    for A in class_inherit_method: 
        new_class_inherit_method[A] = list()
        descendants[A] = list()

    #print(new_class_inherit_method)
   # new_class_inherit_method = class_inherit_method
    #print(new_class_inherit_method)
    visited = []
    for node in inheritance_tree:
        if len(inheritance_tree[node]) == 0:
            BFS1(child_tree, node, visited, new_class_inherit_method,class_inherit_method)
            #descendants_count()
    
    visited1 = []  
    for node in inheritance_tree:
        if len(inheritance_tree[node]) == 0:
            descendants_count(child_tree, node, visited1, descendants,class_inherit_method)     
    #print(class_inherit_method)
    #print( descendants)
    inherit_count = {}
    MOF= 0.0
    for node in new_class_inherit_method:
        #inherit_count[node] = len(set(class_inherit_method[node])-set(class_to_method[node]))
        #print(node)
        #print(set(new_class_inherit_method[node]))
        #print(set(class_to_method[node]))
        #print(len(set(class_inherit_method[node]).intersection(set(class_to_method[node]))))
        overriding_method = len(set(new_class_inherit_method[node]).intersection(set(class_to_method[node])))
        new_method = len(set(class_to_method[node])) - overriding_method
        if len(descendants[node]) != 0:
            MOF += (overriding_method/(new_method*len(set(descendants[node]))))
        #print(overriding_method)
        #print(new_method)
    print("MOF ",MOF)

def coupling_factor(inheritance_tree, child_tree, astree):
    all_classes = []
    couple_all = []
    for classes in astree:
        all_classes.append(classes.name)
    #print(all_classes)
    for class_obj in astree:
        #print("Class Name: ", class_obj.name)
        variable_count = 0
        private_var_count = 0
        class_attr= set()
        class_pr_attr = set()
        #print(class_obj.)
        for func_obj in class_obj.body:
            #print(func_obj.body)
            for statements in func_obj.body:
                if isinstance(statements,ast.Assign):
                    #print(statements.value)
                    for variables in statements.targets:
                        #print(statements.targets)
                        if isinstance(variables,ast.Tuple):
                            if isinstance(variables, ast.Attribute):
                                #print(variables.id)
                                if variables.attr[0] == "_":
                                    class_attr.update(variables.attr)
                                    class_pr_attr.update(variables.attr)
                                else:
                                    class_attr.update(variables.attr)
                            else:
                                for var in variables.elts:
                                    #print(var.id)
                                    variable_count+=1
                                    if var.id[0] == "_":
                                        private_var_count+=1
                        elif isinstance(variables,ast.Name):
                            #print(variables.id)
                            #print(variables.id)
                            variable_count+=1
                            if variables.id[0] == "_":
                                private_var_count+=1
                        elif isinstance(variables, ast.Attribute):
                            #print(variables.attr)
                            if variables.attr[0] == "_":
                                class_attr.update(variables.attr)
                                class_pr_attr.update(variables.attr)
                            else:
                                class_attr.update(variables.attr)
        variable_count +=len(class_attr)
        private_var_count +=len(class_pr_attr)
        #print(class_obj.name)
        #print(class_attr)
        #print(class_pr_attr)
        couple = 0
        
        for second in all_classes:
            if class_obj.name != second and (second in class_attr or second in class_pr_attr):
                couple += 1
        couple_all.append(couple)
    #print(couple_all)
    CF = 0.0
    couple_sum = 0.0
    for i in couple_all:
        couple_sum += i
    dc_sum = 0.0
    #print(child_tree)
    for i in child_tree:
        dc_sum += len(child_tree[i])
    #print(dc_sum)
    devide = (((len(all_classes)*len(all_classes))-len(all_classes)-2*dc_sum))
    if devide != 0:
        CF = (couple_sum / devide)
    print("CF ",CF)

    

inheritance_tree, all_node, astree = inheritance_tree(mdef)    
DIT = depth_of_inheritance_tree_util(inheritance_tree, 0, 0)
print("DIT",DIT)
child_tree = Number_of_child(inheritance_tree, all_node)
print("Number Of Child",child_tree)
attr_hiding_factor(astree)
method_hiding_factor(astree)
method_inheritance_factor(inheritance_tree, child_tree, astree)
attr_inheritance_factor(inheritance_tree, child_tree, astree)
polymorphism_factor(inheritance_tree, child_tree, astree)
coupling_factor(inheritance_tree, child_tree, astree)