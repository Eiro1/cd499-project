import json
import itertools
import Visualization_Plotly


class CourseTreeNode:
    def __init__(self, name, parents, select_child):
        self.name = name
        self.children = []
        self.parents = parents
        self.selectChild = select_child

    def add_child(self, child):
        self.children.append(child)



class CoursePlanTree:
    def __init__(self, name, parents, select_child):
        self.root = CourseTreeNode(name, parents,select_child)
        self.chosen_courses = []

    def print_tree(self, node, level=0):
        if node:
            if isinstance(node.name,tuple):
                for i in node.name:
                    if isinstance(i,str):
                        print("  " * level + f"{i}")
                    else:
                        self.print_tree(i, level )
                print("  " * level+"===========================================")
            else:
                print("  " * level + f"{node.name}:")
                for child in node.children:
                    self.print_tree(child, level + 1)
    # 更新（lxd）

    def create_plan(self, plan_name, stages, parents):
        plan_node = CourseTreeNode(plan_name, parents,"All")
        for stage_name, courses in stages.items():
            stage_node = CourseTreeNode(stage_name, plan_node, str(courses["num"]))
            coursesList= courses["list"]
            for plan in coursesList:
                #如果plan是tree的leaf（lxd）
                if isinstance(plan, str):
                    course_node = CourseTreeNode(plan, stage_node,'leaf')
                    stage_node.add_child(course_node)

                #如果存在sub plan（lxd）
                elif isinstance(plan, dict):
                    stage_node.add_child(self.create_plan(plan["name"], plan["subplan"], stage_node))
            plan_node.add_child(stage_node)
        return plan_node

    def add_plan(self,plan_name, stages):
        plan_node=self.create_plan(plan_name, stages, self.root)
        self.root.add_child(plan_node)

    def find_path(self,node):
        parents = []
        current_node = node
        while current_node.parents is not None:
            parents.append(current_node.parents.name)
            current_node = current_node.parents
        return parents

    def traverse_tree(self, root):
        if not root:
            return []

        result = [root]
        for child in root.children:
            result.extend(self.traverse_tree(child))
        return result


    def enroll_course(self, chosen_courses, course_name):
        with open('course.json') as json_file:
            course_data = json.load(json_file)
    
        # Check if course exists
        course_exists = False
        for course in course_data['courses']: 
            if course['name'] == course_name:
                course_exists = True
                pre_list = course['pre'].split(', ')
                exc_list = course['exclusion'].split(', ')
                break
        
        if not course_exists:
            return "Course not exists"
        
        print("Pre-requisite courses:", pre_list) 
        print("Exclusion courses:", exc_list)
        if pre_list==[""]:
            pre_list=[]
        # Check prerequisites
        if all(course in chosen_courses for course in pre_list):
            if exc_list and any(course in chosen_courses for course in exc_list):
                print("Chosen courses:", chosen_courses)
                return "Enroll failed due to course exclusion"
            if course_name in chosen_courses:
                print("Chosen courses:", chosen_courses)
                return "Enroll failed. it already in chosen_courses"
        
            chosen_courses.append(course_name)
            print("Chosen courses:", chosen_courses)
            return "Enroll success"
        else:
            print("Chosen courses:", chosen_courses)
            return "Enroll failed due to missing prerequisites"

    def print_chosen_courses(self, chosen_courses):
        print("Chosen Courses:")
        for course in chosen_courses:
            print(course)


# Example usage
if __name__ == "__main__":

    # Create the course plan tree
    course_tree = CoursePlanTree("Computing",None,"All")
    #loaddata

    with open('gba.json') as json_file:
        gba_data = json.load(json_file)
    with open('gbc.json') as json_file:
        gbc_data = json.load(json_file)
    with open('mbc.json') as json_file:
        mbc_data = json.load(json_file)
    with open('ssd.json') as json_file:
        ssd_data = json.load(json_file)
    with open('scm.json') as json_file:
        scm_data = json.load(json_file)
    with open('sca.json') as json_file:
        sca_data = json.load(json_file)
    with open('sbc.json') as json_file:
        sbc_data = json.load(json_file)
    with open('sco.json') as json_file:
        sco_data = json.load(json_file)
    with open('scs.json') as json_file:
        scs_data = json.load(json_file)
    #add plan

    course_tree.add_plan("Computing–General", gbc_data['gbc'])
    course_tree.add_plan("Computing–General (Arts)", gba_data['gba'])
    course_tree.add_plan("Major(Computing)", mbc_data['mbc'])
    course_tree.add_plan("Software Design–Specialization", ssd_data['ssd'])
    course_tree.add_plan("Computing, Mathematics and Analytics–Specialization (Computing)", scm_data['scm'])
    course_tree.add_plan("Computing and the Creative Arts - Specialization", sca_data["sca"])
    course_tree.add_plan("Biomedical Computing – Specialization", sbc_data["sbc"])
    course_tree.add_plan("Cognitive Science – Specialization", sco_data["sco"])
    course_tree.add_plan("Computer Science–Specialization", scs_data["scs"])

    # Print the tree
    #course_tree.print_tree(course_tree.root)

    # 获取总图可视化参数
    result = course_tree.traverse_tree(course_tree.root)
    data = {'parents': [''], 'value': [900.0], 'title': 'graph of Course-Curriculum Map',
             'ids': ['Computing'], 'labels': ['Computing']}
    for i in result:
        if i != course_tree.root:
            #获取tree——node 的 路径并将其作为name
            path_node = course_tree.find_path(i)
            path_parents = course_tree.find_path(i.parents)
            node_name = i.name
            if i.selectChild != "leaf":
                data["labels"].append(i.name+"(complete "+i.selectChild+ " from children)")
            else: data["labels"].append(i.name)
            parents_name = i.parents.name
            for j in path_node:
                node_name += "-" + j
            data['ids'].append(node_name)
            for j in path_parents:
                parents_name += "-" + j
            data['parents'].append(parents_name)
            parentsId = data['ids'].index(parents_name)
            value = data['value'][parentsId]/len(i.parents.children)
            data['value'].append(value)
    #旭日图可视化
    Visualization_Plotly.total_sunburst(data)

    #分支图可视化参数
    for i in course_tree.root.children:

        nodelist = course_tree.traverse_tree(i)
        node_data = {"label": [], "color": []}
        link_data = {'source': [], "target": [], "value": [] , "color":[]}
        for node in nodelist:

            if node.selectChild != 'leaf':
                node_name = node.name+"(complete "+ node.selectChild + " from children)"
                node_data["label"].append(node_name)
                if node.parents.name == "Computing":
                    node_data["color"].append("blue")
                else:
                    node_data["color"].append("red")
                    link_data['source'].append(nodelist.index(node))
                    link_data['target'].append(nodelist.index(node.parents))
                    link_data['value'].append(0.3)
                    link_data["color"].append("rgba(255,0,255, 0.3)")

            else:
                node_name = node.name
                node_data["label"].append(node_name)
                node_data["color"].append("yellow")
                link_data['source'].append(nodelist.index(node))
                link_data['target'].append(nodelist.index(node.parents))
                link_data['value'].append(0.3)
                link_data["color"].append("rgba(255, 0, 255, 0.3)")

        for node in nodelist:
            if node.selectChild=='leaf':
                with open('course.json') as f:
                    course_data = json.load(f)
                for course_dict in course_data["courses"]:
                    if node.name==course_dict["name"] and course_dict["pre"] != "":
                        pre = course_dict['pre'].split(', ')
                        for i in pre:
                            if i not in node_data["label"]:
                                node_data["label"].append(i)
                                node_data["color"].append("yellow")
                                link_data['source'].append(nodelist.index(node))
                                link_data['target'].append(len(node_data["label"])-1)
                                link_data['value'].append(0.3)
                                link_data["color"].append("rgba(200, 200, 255, 0.6)")
                            else:
                                link_data['source'].append(nodelist.index(node))
                                link_data['target'].append(node_data["label"].index( i ) )
                                link_data['value'].append(0.3)
                                link_data["color"].append("rgba(200, 200, 255, 0.6)")

        Visualization_Plotly.sankey(node_data, link_data)
    # Enroll in a course
    print(course_tree.enroll_course(course_tree.chosen_courses, "CISC121"))
    print(course_tree.enroll_course(course_tree.chosen_courses, "CISC220"))
    print(course_tree.enroll_course(course_tree.chosen_courses, "CISC124"))
    print(course_tree.enroll_course(course_tree.chosen_courses, "CISC124"))
    # Print chosen courses
    course_tree.print_chosen_courses(course_tree.chosen_courses)
