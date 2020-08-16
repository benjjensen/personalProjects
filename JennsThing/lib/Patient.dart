import 'Parameters.dart';

class Patient {
  var patientWeight;
  var caloricNeeds_min;
  var caloricNeeds_max;
  var proteinNeeds_min;
  var proteinNeeds_max;
  var scaledCaloricNeeds_min;
  var scaledCaloricNeeds_max;

  var averageCaloricNeeds;
  var averageProteinNeeds;
  var averageProteinRounded;

  List<double> aminoAcidSolution = [];

  var hourlyRate = [];
  var updatedVolume = [];
  var updatedProtein = [];
  var updatedCalories = [];

  void calculateNutrientNeeds() {
    caloricNeeds_min = caloriesPerKg_lower * patientWeight; // in kcal/day
    caloricNeeds_max = caloriesPerKg_upper * patientWeight;

    proteinNeeds_min = proteinPerKg_lower * patientWeight; // in g / day
    proteinNeeds_max = proteinPerKg_upper * patientWeight;

    scaledCaloricNeeds_min =
        caloricNeeds_min * parenteralScalingFactor; // in kcal / day
    scaledCaloricNeeds_max = caloricNeeds_max * parenteralScalingFactor;

    averageCaloricNeeds =
        (scaledCaloricNeeds_min + scaledCaloricNeeds_max) / 2.0;
    averageProteinNeeds = (proteinNeeds_min + proteinNeeds_max) / 2.0;
    averageProteinRounded = averageProteinNeeds.round();
  }

  void determineSolutionVolume() {
    for (int i = 0; i < aminoAcidConcentrations.length; i++) {
      aminoAcidSolution.add(averageProteinRounded / aminoAcidConcentrations[i]);
    }
  }

  void determineHourlyRate() {
    for (int i = 0; i < aminoAcidConcentrations.length; i++) {
      // Round to the nearest 5 for each concentration (divide by 5, round, multiply by 5 again)
      hourlyRate.add(
          ((aminoAcidSolution[i] / rateOfGiving) / portionRounding).round() *
              portionRounding);

      // Update volume with rounded values
      updatedVolume.add(rateOfGiving * hourlyRate[i]);

      // Update the total protein provided
      updatedProtein.add(updatedVolume[i] * aminoAcidConcentrations[i]);

      // Update the calories provided
      updatedCalories.add(updatedProtein[i] * caloriesPerProtein);
    }
  }

  void determineLipids() {}

  void doItAll() {
    aminoAcidSolution.clear();
    hourlyRate.clear();
    updatedVolume.clear();
    updatedProtein.clear();
    updatedCalories.clear();

    calculateNutrientNeeds();
    determineSolutionVolume();
    determineHourlyRate();
  }

  void setPatientWeight(String weight) {
    patientWeight = double.parse(weight); // in kg
  }

  int getCalories() {
    return caloricNeeds_min;
  }
}
