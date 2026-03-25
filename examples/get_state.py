print('document:', document.name if document else None)
print('has design:', design is not None)
print('root component:', rootComp.name if rootComp else None)
result = {
    'documentName': document.name if document else None,
    'hasDesign': design is not None,
    'rootComponentName': rootComp.name if rootComp else None,
}
