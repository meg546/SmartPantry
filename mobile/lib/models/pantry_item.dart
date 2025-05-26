class PantryItem {
  final int id;
  final String name;
  final int quantity;
  final String unit;
  final DateTime addedDate;
  final String? barcode;

  PantryItem({
    required this.id,
    required this.name,
    required this.quantity,
    required this.unit,
    required this.addedDate,
    this.barcode,
  });

  factory PantryItem.fromJson(Map<String, dynamic> json) {
    return PantryItem(
      id: json['id'],
      name: json['name'],
      quantity: json['quantity'],
      unit: json['unit'],
      addedDate: DateTime.parse(json['added_date']),
      barcode: json['barcode'],
    );
  }

  Map<String, dynamic> toJson() {
    return {
      'id': id,
      'name': name,
      'quantity': quantity,
      'unit': unit,
      'added_date': addedDate.toIso8601String(),
      'barcode': barcode,
    };
  }
}